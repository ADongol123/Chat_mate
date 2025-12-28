from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
from app.utils.config import settings

QDRANT_URL = settings.QDRANT_URL
QDRANT_API_KEY = settings.QDRANT_API_KEY

class ProductRetriever:
    """
    Handles real product retrieval from Qdrant.
    """
    def __init__(self, host="localhost", port=6333, collection_name="products"):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        
        self.collection_name = collection_name

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_meta: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Perform semantic search in Qdrant.
        query_vector: embedding vector from LLM/encoder
        filter_meta: optional dict for metadata filtering, e.g., {"category": "Headphones"}
        """
        # Build filter if metadata provided
        q_filter = None
        if filter_meta:
            must_conditions = []
            for k, v in filter_meta.items():
                must_conditions.append(models.FieldCondition(key=k, match=models.MatchValue(value=v)))
            q_filter = models.Filter(must=must_conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=q_filter
        )

        # Return list of products
        products = []
        for hit in results:
            product = hit.payload
            product["score"] = hit.score  # optional similarity score
            products.append(product)
        return products
