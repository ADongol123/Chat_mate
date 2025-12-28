from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Query
from langchain_huggingface import HuggingFaceEmbeddings
from app.utils.auth import get_current_user
from app.core.ecom_parsing import detect_file_type, read_file, dataframe_to_text_list
from app.qdrant.collection import get_qdrant_client, safe_collection_exists
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from app.utils.config import settings
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient
from concurrent.futures import ThreadPoolExecutor
from app.core.intent_classification import classify_intent_with_mistral
import traceback


app = APIRouter(prefix="/Ecom_Bots", tags=["Chatbots"])
EMBEDDER = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Async MongoDB client
mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongo_db = mongo_client[settings.DB_NAME]


executor = ThreadPoolExecutor()

embeddings_collection = mongo_db[settings.COMPANY_DATA_COLLECTION]

# Helper function to run blocking tasks
async def run_in_executor(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func)

INTENT_COLLECTION_MAPPING = {
    "product_search": "products",
    "product_comparison": "products",
    "product_recommendation": "products",
    "product_availability": "products",
    "product_details": "products",
    "discount_inquiry": "promotions",
    "price_check": "promotions",
    "promotions": "promotions",
    "order_tracking": "orders",
    "order_modification": "orders",
    "order_issue": "orders",
    "delivery_inquiry": "orders",
    "return_request": "returns",
    "refund_status": "returns",
    "payment_methods": "billing",
    "billing_issue": "billing",
    "invoice_request": "billing",
    "account_creation": "account",
    "account_login": "account",
    "account_update": "account",
    "technical_issue": "support",
    "app_support": "support",   
    "store_policy": "store",
    "store_info": "store",
    "subscription_inquiry": "store",
    "greeting_smalltalk": "misc",
    "feedback_complaint": "misc",
    "agent_escalation": "misc", 
    "unknown": "misc"
}


@app.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    bot_type: str = "general",
    data_type: str = "default",
    user_id: str = Depends(get_current_user)
):
    # Step 1: Parse the file
    try:
        file_type = detect_file_type(file)
        df = read_file(file, file_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parsing failed: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or invalid")

    # Step 2: Convert dataframe to texts and generate embeddings
    texts = dataframe_to_text_list(df)
    embeddings = EMBEDDER.embed_documents(texts)
    vector_size = len(embeddings[0])

    # Step 3: Generate payloads
    payloads = []
    for i, row in df.iterrows():
        metadata = row.to_dict()
        metadata["bot_type"] = bot_type
        payloads.append(metadata)

    # Step 4: Store in Qdrant
    qdrant = get_qdrant_client()
    collection_name = f"user_{user_id}_{bot_type}"

    if not safe_collection_exists(qdrant, collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    # Batch insert to prevent server disconnect
    BATCH_SIZE = 200
    points = [
        PointStruct(
            id=hashlib.md5(f"{user_id}_{i}".encode()).hexdigest(),
            vector=embeddings[i],
            payload=payloads[i]
        ) for i in range(len(texts))
    ]
    try:
        for i in range(0, len(points), BATCH_SIZE):
            qdrant.upsert(collection_name=collection_name, points=points[i:i+BATCH_SIZE])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upsert to Qdrant: {str(e)}")

    # Step 5: Async MongoDB insert
    mongo_records = [
        {"user_id": user_id, "bot_type": bot_type, "data_type": data_type,
         "text": texts[i], "metadata": payloads[i]}
        for i in range(len(texts))
    ]
    try:
        await embeddings_collection.insert_many(mongo_records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert to MongoDB: {str(e)}")

    return {
        "message": "File processed successfully. Embeddings stored in Qdrant and MongoDB.",
        "records": len(texts),
        "columns_used": df.columns.tolist(),
        "collection_name": collection_name
    }




@app.get("/search")
async def search_text(
    query: str = Query(..., min_length=3),
    k: int = 5,
    user_id: str = Depends(get_current_user)
):
    try:
        # Step 1: Detect intent
        classification = classify_intent_with_mistral(query)
        print("Classification result:", classification)
        intent = classification.get("intent", "unknown")
        print(f"[INFO] Query intent detected: {intent}")

        # Step 2: Map intent -> data collection
        data_type = INTENT_COLLECTION_MAPPING.get(intent, "misc")
        collection_name = f"user_{user_id}_{intent}"
        print(collection_name)
        # Step 3: Verify collection exists
        qdrant = get_qdrant_client()
        if not safe_collection_exists(qdrant, collection_name):
            raise HTTPException(
                status_code=404,
                detail=f"No data found for user {user_id} with data type {data_type}"
            )

        # Step 4: Embed query & search in Qdrant
        query_embedding = EMBEDDER.embed_query(query)
        search_result = qdrant.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            limit=k
        )

        # Step 5: Optionally enrich results from MongoDB
        enriched_results = []
        for hit in search_result:
            mongo_doc = await embeddings_collection.find_one({
                "text": hit.payload.get("text")
            })
            enriched_results.append({
                "score": hit.score,
                "payload": hit.payload,
                "mongo_metadata": mongo_doc
            })

        return {
            "query": query,     
            "intent": intent,
            "collection_used": collection_name,
            "results": enriched_results
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
