from fastapi import APIRouter, HTTPException
from app.schemas.auth_schema import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user


app = APIRouter(prefix="/auth", tags=["Authentication"])

@app.post("/register")
async def register(data: UserRegister):
    try:
        result = await register_user(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    


@app.post("/login")
async def login(data: UserLogin):
    try:
        result = await login_user(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# @app.post("/create_tenant")
# async def create_tenant():