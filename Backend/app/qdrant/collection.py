from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance


# Initialize the client
client  = QdrantClient(host="localhost", port=6333)

# Define the collection name
collection_name = "my_documents"
vector_size = 768
distance_metric = Distance.COSINE


# Create the collection 
client.recreate_collection(
    collection_name=collection_name,
    vector_config = VectorParams(size=vector_size, distance=distance_metric)
)