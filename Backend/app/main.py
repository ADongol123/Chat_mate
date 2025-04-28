# from fastapi import FastAPI
# from app.api.chatbot import chatbot, tenant, user, auth
# app  = FastAPI()

# app.include_router(chatbot.router, prefix="/api/v1/chatbots", tags=["Chatbots"])
# app.include_router(tenant.router, prefix="/api/v1/tenants", tags=["Tenants"])
# app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
import uvicorn
from fastapi import FastAPI
from app.routes.ai_routes import router as ai_router  # import your router
from app.api.dataParsing import app as data_routes
app = FastAPI()

# Include the ai_routes router
app.include_router(ai_router)
app.include_router(data_routes)


@app.get("/")
async def root():
    return {"message": "Welcome to the Intent API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
