from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from app.utils.config import settings
from langchain_huggingface import HuggingFaceEmbeddings
from app.db.database import db
user_vectorstore_cache = {}
embeddings_collection = db["embeddings"]

# Embedding model for text
accurate_model_id = 'all-mpnet-base-v2'
accurate_embedding_model = HuggingFaceEmbeddings(model_name=accurate_model_id)

QDRANT_URL = settings.QDRANT_URL
QDRANT_API_KEY = settings.QDRANT_API_KEY
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_vectorstore(user_id: str):
    collection_name = f"user_{user_id.replace('-','_')}"
    
    if user_id in user_vectorstore_cache:
        return user_vectorstore_cache[user_id]
    
    if not qdrant_client.collection_exists(collection_name):
        raise ValueError(f"No data uplaoded for user {user_id}. Please upload file first")
    
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=accurate_embedding_model
    )
    
    user_vectorstore_cache[user_id] = vectorstore
    return vectorstore