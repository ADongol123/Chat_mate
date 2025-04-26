from fastapi import FastAPI
from app.api.chatbot import chatbot, tenant, user, auth


app  = FastAPI()

app.include_router(chatbot.router, prefix="/api/v1/chatbots", tags=["Chatbots"])
app.include_router(tenant.router, prefix="/api/v1/tenants", tags=["Tenants"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])