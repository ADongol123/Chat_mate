from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct,VectorParams, Distance
import csv
import uuid
from app.utils.image_clip_utils import  get_clip_text_embedding
# Initialize the client
qdrant  = QdrantClient(host="localhost", port=6333)

# Define the collection name
collection_name = "my_documents"
vector_size = 768
distance_metric = Distance.COSINE


# # Create the collection 
# client.recreate_collection(
#     collection_name=collection_name,
#     vector_config = VectorParams(size=vector_size, distance=distance_metric)
# )





def upload_csv_to_qdrant(csv_path: str, user_id: str):
    collection_name = f"user_{user_id.replace('-', '_')}"
    
    # Create collection (512 = CLIP ViT-B-32 vector size)
    if not qdrant.collection_exists(collection_name):
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE)
        )

    points = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            asin, title, image_url, product_url, *_ = row
            embedding = get_clip_text_embedding(title)
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "asin": asin,
                    "text": title,
                    "image_url": image_url,
                    "product_url": product_url
                }
            ))
    
    qdrant.upsert(collection_name=collection_name, points=points)
    print(f"✅ Uploaded {len(points)} products to Qdrant for user {user_id}")