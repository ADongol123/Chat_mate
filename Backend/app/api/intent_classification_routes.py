from app.core.intent_classification import classify_intent_with_mistral
from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

app = APIRouter(prefix="/intent", tags=["E-commerce_intent_classification"])

class IntentRequest(BaseModel):
    query: str
    
@app.post("/classify")
def classify_intent(request: IntentRequest):
    try:
        classification = classify_intent_with_mistral(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error classifying intent: {str(e)}")
        
    return classification
                    