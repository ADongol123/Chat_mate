from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.api.chat.chat_utils import PyObjectId

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

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

class ChatbotCreate(ChatBotBase):
    pass

class Chatbot(ChatBotBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
    }
    
    
    
class ChatbotUpdate(ChatBotBase):
    pass

class ChatbotResponse(ChatBotBase):
    id: str
    owner: str
    model_config = {
        "populate_by_name": True,
    }
