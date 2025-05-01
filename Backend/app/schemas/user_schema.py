from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime 

class UserRole(str, Enum):
    ADMIN = "admin"
    TENANT = "tenant"
    


class AccountType(str, Enum):
    FREE = "free"
    PAID = "paid"
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.TENANT
    account_type : AccountType 
    has_paid: bool = False
    created_at: datetime = datetime.utcnow()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    
    
    
class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr
    role: UserRole
    tenant_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
    


