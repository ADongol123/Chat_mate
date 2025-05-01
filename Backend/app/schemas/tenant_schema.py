from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime 

class TenantCreate(BaseModel):
    name: str
    contact_email : EmailStr
    domain: str  # e.g., business-name.com
    description: Optional[str] = None

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None

class TenantOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    domain: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True