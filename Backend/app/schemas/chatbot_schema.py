from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime 



class ChatbotCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tenant_id: str  # Chatbots are tied to a tenant
    intents: Optional[List[str]] = []

class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    intents: Optional[List[str]] = None

class ChatbotOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    description: Optional[str] = None
    tenant_id: str
    intents: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True