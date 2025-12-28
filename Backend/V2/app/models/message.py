from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserMessage(BaseModel):
    session_id: str
    message:str
    timestamp: Optional[datetime] = None
    
    

class BotMessage(BaseModel):
    session_id: str
    message: str
    timestamp: datetime