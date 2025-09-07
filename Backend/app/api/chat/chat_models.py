from pydantic import BaseModel
from fastapi import Optional, EmailStr
from datetime import datetime 
from typing import List
from app.api.chat.chat_utils import PyObjectId
from bson import ObjectId



class ChatBotBase(BaseModel):
    name: str
    description: Optional[str] = ""
    templates: List[str] = []
    primaryColor: str = "#0070f3"
    secondaryColor: str = "#f5f5f5"
    welcomeMessage: str = "Hi there! How can I help you today?"
    autoShow: bool = False
    delayTime: int = 5
    collectEmail: bool = True
    fallbackContact: bool = True
    
    



class ChatbotCreate(ChatBotBase):
    pass

class Chatbot(ChatBotBase):
    id: PyObjectId
    user_email: EmailStr
    created_at: datetime
    updated_at: datetime
    
    
class ChatbotUpdate(ChatBotBase):
    pass


class ChatbotResponse(ChatBotBase):
    id: str
    owner: str
    


class Config:
    json_encoders = {ObjectId: str}
