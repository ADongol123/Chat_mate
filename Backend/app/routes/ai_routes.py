import sys
import pandas as pd
from app.utils.ai_data_load import load_intent_data
from fastapi import APIRouter

router  = APIRouter()


file_path = "app/data/intent_dataset.json"

intent_data = load_intent_data(file_path)

unique_intents = pd.DataFrame(intent_data)['intent'].unique()


for intent in unique_intents:
    async def intent_route(intent_name= intent):
        filtered_queries = [item["query"] for item in intent_data if item['intent'] == intent_name]
        return {"intent": intent_name, "queries":filtered_queries}
    
    # Register dynamic route
    router.add_api_route(f"/intent/{intent}",intent_route, methods=['GET'])
    
    

@router.get("/test")
async def test():
    return {"message":"This is a test route!"}