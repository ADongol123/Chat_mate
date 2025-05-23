from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException, Query, Depends
import pandas as pd
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from app.core.ecom_parsing import detect_file_type, read_file, dataframe_to_text_list, select_text_columns
from langchain_community.vectorstores import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from app.utils.auth import get_current_user
from app.db.database import db
from langchain.schema import Document
import numpy as np
import os
import asyncio
import traceback
from qdrant_client import QdrantClient
from concurrent.futures import ThreadPoolExecutor
from app.utils.config import settings
executor = ThreadPoolExecutor(max_workers=os.cpu_count() * 2)

class Query_values(BaseModel):
    question: str
    top_k: int = 5

app = APIRouter(prefix="/ecom", tags=["E-commerce"])

user_vectorstore_cache = {}
embeddings_collection = db["embeddings"]

# Embedding model
accurate_model_id = 'all-mpnet-base-v2'
accurate_embedding_model = HuggingFaceEmbeddings(model_name=accurate_model_id)

# Qdrant settings
QDRANT_URL =  settings.QDRANT_URL 
QDRANT_API_KEY = settings.QDRANT_API_KEY  
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

async def run_in_executor(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func)

async def get_user_embeddings_from_db(user_id: str):
    cursor = embeddings_collection.find({"user_id": user_id})
    results = await cursor.to_list(length=None)

    if not results:
        return [], [], []

    texts = [doc["text"] for doc in results]
    metadata = [doc.get("metadata", {}) for doc in results]
    embeddings = [doc["embedding"] for doc in results]

    return texts, embeddings, metadata

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    try:
        file_type = detect_file_type(file)
        df = read_file(file, file_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing failed: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or invalid")

    product_texts = dataframe_to_text_list(df)
    product_metadata = df.to_dict(orient="records")

    docs = [Document(page_content=text, metadata=product_metadata[i]) for i, text in enumerate(product_texts)]
    collection_name = f"user_{user_id.replace('-', '_')}"

    try:
        if qdrant_client.collection_exists(collection_name):
            qdrant_client.delete_collection(collection_name)

        vectorstore = Qdrant.from_documents(
            docs,
            accurate_embedding_model,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=collection_name
        )

        user_vectorstore_cache[user_id] = vectorstore
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector index creation failed: {str(e)}")

    embeddings = accurate_embedding_model.embed_documents(product_texts)
    records_to_save = [
        {
            "user_id": user_id,
            "text": text,
            "embedding": embeddings[i],
            "metadata": product_metadata[i]
        } for i, text in enumerate(product_texts)
    ]

    await embeddings_collection.insert_many(records_to_save)

    return {
        "message": "File processed successfully. Embeddings and Qdrant index generated and stored.",
        "records": len(product_texts),
        "columns_used": select_text_columns(df)
    }

@app.get("/search")
async def search(query: str = Query(..., min_length=3), k: int = 5, user_id: str = Depends(get_current_user)):
    collection_name = f"user_{user_id.replace('-', '_')}"

    try:
        if user_id in user_vectorstore_cache:
            vectorstore = user_vectorstore_cache[user_id]
        else:
            vectorstore = Qdrant(
                client=qdrant_client,
                collection_name=collection_name,
                embeddings=accurate_embedding_model
            )
            user_vectorstore_cache[user_id] = vectorstore

        results = await run_in_executor(
            lambda: vectorstore.similarity_search(query, k=k)
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

    return {"results": [
        {"text": doc.page_content, "metadata": doc.metadata} for doc in results
    ]}
