from pydantic import BaseModel
from typing import Optional, Dict

class Intent(BaseModel):
    name:str
    confidence:float
    slots: Optional[Dict] = {}