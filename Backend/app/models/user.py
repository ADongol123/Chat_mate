from pydantic import BaseModel,EmailStr

class User(BaseModel):
    email: EmailStr
    full_name: str = None
    hashed_password: str =None
    is_google_user: bool = False