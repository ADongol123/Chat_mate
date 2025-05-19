from fastapi import FastAPI, UploadFile, File,APIRouter, HTTPException
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import tempfile
import os
from pydantic import BaseModel
from app.core.ecom_parsing import save_temp_file, load_and_clean_csv, parse_product_text ,detect_file_type,read_file,dataframe_to_text_list
from app.core.ecom_embeddings import generate_embeddings, create_faiss_index
class Query(BaseModel):
    question: str
    top_k: int = 5
    
app = APIRouter(prefix="/ecom", tags=["E-commerce"])
    
# app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use other models

# Store in-memory DB for simplicity
product_texts = []
product_metadata = []
index = None

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    global product_texts, product_metadata, index

    try:
        file_type = detect_file_type(file)
        df = read_file(file, file_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    product_texts = dataframe_to_text_list(df)

    # Store full product metadata
    product_metadata = df.to_dict(orient='records')


    embeddings = model.encode(product_texts, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return {
        "message": "File processed successfully.",
        "records": len(product_texts)
    }



@app.get("/search")
def search_products(query: str):
    global product_texts, product_metadata, index

    if not product_texts or index is None:
        raise HTTPException(status_code=400, detail="No data available. Upload a file first.")

    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k=5)
    results = [product_metadata[i] for i in I[0]]

    return {"results": results}
