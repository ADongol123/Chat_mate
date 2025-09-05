from app.utils.vector_store import get_vectorstore
from app.api.ecom_routes import rerank_with_mistral,run_in_executor
async def handle_discount_inquiry(query:str,user_id: str):
    """
    handle discount-related queries using Qdrant vector search
    """
    vectorstore = get_vectorstore(user_id)
    
    # Step 1: Retrieve candidates
    items = await run_in_executor(lambda: vectorstore.similarity_search(query, k=5))
    
    # Step 2: Rerank with Mistral
    selected = rerank_with_mistral(query, items)
    
    # Step 3: Filter by metadata
    results = [doc for doc,score in selected if doc.metadata.get("discount",0)>0]
    
    return results


def handle_price_check(df, entities):
    query = " ".join(entities).lower()
    match = df[df["product_name"].str.lower().str.contains(query, na=False)]
    return {"product": match.iloc[0]["product_name"], "price": match.iloc[0]["price"]} if not match.empty else {"error": "Price not available"}

def handle_promotions(df, entities=None):
    results = df[df["discount"] > 0]
    return results[["product_name", "price", "discount"]].to_dict(orient="records") if not results.empty else {"message": "No promotions available"}
