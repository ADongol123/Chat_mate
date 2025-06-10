from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException, Query, Depends, Form
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
from typing import Optional # Import Optional for the new endpoint
from torchvision import models, transforms # For image processing
from PIL import Image # For image processing
import io # For image processing
import torch # For image processing

executor = ThreadPoolExecutor(max_workers=os.cpu_count() * 2)

class Query_values(BaseModel):
    question: str
    top_k: int = 5

app = APIRouter(prefix="/ecom", tags=["E-commerce"])

user_vectorstore_cache = {}
embeddings_collection = db["embeddings"]

# Embedding model for text
accurate_model_id = 'all-mpnet-base-v2'
accurate_embedding_model = HuggingFaceEmbeddings(model_name=accurate_model_id)

# Qdrant settings
QDRANT_URL = settings.QDRANT_URL
QDRANT_API_KEY = settings.QDRANT_API_KEY
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# --- Image embedding model and functions ---
# Load a pre-trained ResNet model for image embeddings
resnet_model = models.resnet50(pretrained=True)
# Set the model to evaluation mode (important for inference)
resnet_model.eval()

class ResNetFeatureExtractor(torch.nn.Module):
    def __init__(self, original_model, output_dim):
        super().__init__()
        # Take all layers except the last classification layer (avgpool + fc)
        self.features = torch.nn.Sequential(*(list(original_model.children())[:-1]))
        # Add a linear layer to project to the desired output dimension
        self.projection = torch.nn.Linear(2048, output_dim) # ResNet50 outputs 2048 features before FC

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1) # Flatten the output of avgpool (e.g., from [batch, 2048, 1, 1] to [batch, 2048])
        x = self.projection(x)
        return x

# Instantiate our custom feature extractor
# Make sure the output_dim matches your text embedding dimension (768)
image_feature_extractor = ResNetFeatureExtractor(resnet_model, output_dim=768)
image_feature_extractor.eval() # Set to evaluation mode

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def get_image_embedding(image_bytes):
    """
    Generates a vector embedding for an image, projected to 768 dimensions.
    Args:
        image_bytes: Bytes of the image file.
    Returns:
        A list representing the 768-dimensional image embedding.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = image_transform(image).unsqueeze(0)
        with torch.no_grad():
            # Use the new image_feature_extractor
            embedding = image_feature_extractor(tensor).squeeze().numpy()
        return embedding.tolist()
    except Exception as e:
        print(f"Error generating image embedding: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Image embedding failed: {str(e)}")

# --- End Image embedding model and functions ---

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
            accurate_embedding_model, # Using accurate_embedding_model for text embeddings
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=collection_name
        )

        user_vectorstore_cache[user_id] = vectorstore
    except Exception as e:
        traceback.print_exc()
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

    try:
        await embeddings_collection.insert_many(records_to_save)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to save embeddings to database: {str(e)}")

    return {
        "message": "File processed successfully. Embeddings and Qdrant index generated and stored.",
        "records": len(product_texts),
        "columns_used": select_text_columns(df)
    }

# Existing text-only search endpoint (GET)
@app.get("/search/text") # Renamed for clarity to distinguish from image/hybrid search
async def search_text(query: str = Query(..., min_length=3), k: int = 5, user_id: str = Depends(get_current_user)):
    collection_name = f"user_{user_id.replace('-', '_')}"

    try:
        if user_id in user_vectorstore_cache:
            vectorstore = user_vectorstore_cache[user_id]
        else:
            if not qdrant_client.collection_exists(collection_name):
                raise HTTPException(status_code=404, detail=f"No data uploaded for user '{user_id}'. Please upload a file first.")
            vectorstore = Qdrant(
                client=qdrant_client,
                collection_name=collection_name,
                embeddings=accurate_embedding_model
            )
            user_vectorstore_cache[user_id] = vectorstore

        results = await run_in_executor(
            lambda: vectorstore.similarity_search(query, k=k)
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Text search failed: {str(e)}")

    return {"results": [
        {"text": doc.page_content, "metadata": doc.metadata} for doc in results
    ]}


# --- NEW IMAGE/HYBRID SEARCH ENDPOINT (POST) ---
@app.post("/search/image")
async def search_image(
    image: UploadFile = File(...),
    query: Optional[str] = Form(None),
    k: int = Form(5),
    user_id: str = Depends(get_current_user)
):
    collection_name = f"user_{user_id.replace('-', '_')}"
    results_combined = []

    try:
        if user_id in user_vectorstore_cache:
            vectorstore = user_vectorstore_cache[user_id]
        else:
            if not qdrant_client.collection_exists(collection_name):
                raise HTTPException(status_code=404, detail=f"No data uploaded for user '{user_id}'. Please upload a file first.")
            vectorstore = Qdrant(
                client=qdrant_client,
                collection_name=collection_name,
                embeddings=accurate_embedding_model
            )
            user_vectorstore_cache[user_id] = vectorstore

        # 1. Process Image
        image_bytes = await image.read()
        # image_embedding will now be 768 dimensions thanks to the updated get_image_embedding
        image_embedding = await run_in_executor(lambda: get_image_embedding(image_bytes))
        image_embedding_np = np.array(image_embedding) # Shape (768,)

        # 2. Process Text Query (if provided)
        combined_vector = image_embedding_np
        if query:
            text_embedding = await run_in_executor(lambda: accurate_embedding_model.embed_query(query))
            text_embedding_np = np.array(text_embedding) # Shape (768,)

            # Now both embeddings are (768,), so broadcasting will work
            combined_vector = (image_embedding_np + text_embedding_np) / 2

        # 3. Perform Qdrant search
        qdrant_search_results = await run_in_executor(
            lambda: qdrant_client.search(
                collection_name=collection_name,
                query_vector=combined_vector.tolist(),
                limit=k,
                with_payload=True
            )
        )

        results_combined.extend([
            {
                "source": "hybrid" if query else "image_only",
                "text": point.payload.get("text", ""),
                "metadata": point.payload
            }
            for point in qdrant_search_results
        ])

        return {"results": results_combined}

    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Image search failed: {str(e)}")

