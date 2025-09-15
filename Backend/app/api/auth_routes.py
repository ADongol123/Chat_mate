from fastapi import APIRouter, HTTPException, Depends, Request,Form, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token 
from app.db.database import users_collection
from app.models.user import User
from app.utils.config import settings
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm  
# from fastapi import FastAPI
import os
os.environ.pop("SSL_CERT_FILE", None)

router = APIRouter()

# router.add_middleware(SessionMiddleware, secret_key="your_super_secret_key")

# router.include_router(auth_routes.router)
# OAuth configuration

class LoginRequest(BaseModel):
    username: str
    password: str


config_data = {
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
    "SECRET_KEY": settings.SECRET_KEY,
}
config = Config(environ=config_data)
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',  # needed for user info
    client_kwargs={'scope': 'openid email profile'},
    
)

class RegisterModel(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str

@router.post("/auth/register")
async def register(user: RegisterModel):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_pw
    user_dict["is_google_user"] = False
    del user_dict["password"]
    users_collection.insert_one(user_dict)
    return {"msg": "User registered successfully"}


@router.post("/auth/login")
async def login(response: Response, payload:  OAuth2PasswordRequestForm = Depends()): 
    db_user = await users_collection.find_one({"email": payload.username})
    if not db_user or not verify_password(payload.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": payload.username})
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=3600,
        path="/"
    )

    return {"message": "Login successful","email":db_user["email"], "token":token}


@router.get("/auth",name="auth")
async def auth_google(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    email = user_info['email']  
    user = users_collection.find_one({"email": email})
    if not user:
        user_data = {
            "email": email,
            "full_name": user_info.get("name"),
            "hashed_password": None,
            "is_google_user": True
        }
        users_collection.insert_one(user_data)
    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
