from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts: list) -> np.ndarray:
    """Generate embeddings using the SentenceTransformer model."""
    return model.encode(texts, show_progress_bar=True)


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Create and return a FAISS index with the given embeddings."""
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index
