from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts: list) -> np.ndarray:
    """Generate embeddings using the SentenceTransformer model."""
    return model.encode(texts, show_progress_bar=True)


def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexIVFFlat:
    dim = embeddings.shape[1]
    quantizer = faiss.IndexFlatL2(dim)
    index = faiss.IndexIVFFlat(quantizer, dim, nlist=100)  # nlist = number of clusters
    index.train(embeddings)  # Important: train first!
    index.add(embeddings)
    return index




def search_index(query_embedding, index,product_metadata, threshold:0.4):
    query_embedding = np.array([query_embedding]).astype("float32")
    
    
    #FAISS returns (distances, indices)
    distances, indices = index.search(query_embedding, k=5)
    
    
    best_distance = distances[0][0]
    best_index = indices[0][0]
    
    #Check if best distance is below threshold
    if best_distance > threshold:
        return None
    
    return product_metadata[best_index]