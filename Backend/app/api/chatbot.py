from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chatbot_schema import ChatbotCreate
from app.services.chatbot_service import create_chatbot

router = APIRouter()

@router.post("/")
async def create_new_chatbot(chatbot: ChatbotCreate):
    chatbot_data = await create_chatbot(chatbot)
    return {"msg": "Chatbot created", "data": chatbot_data}
