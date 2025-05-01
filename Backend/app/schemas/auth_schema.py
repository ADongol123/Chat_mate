from pydantic import BaseModel, EmailStr, Field
from app.schemas.user_schema import  AccountType,UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    

class UserRegister(BaseModel):
    name:str
    email: EmailStr
    password: str
    account_type: AccountType 
    role: UserRole
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
