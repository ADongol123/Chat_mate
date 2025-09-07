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
from app.api.auth_routes import router as auth_routes
from app.api.tenant import app as tenant_routes
from fastapi.middleware.cors import CORSMiddleware
from app.api.ecom_routes import app as ecom_routes
from app.api.intent_classification_routes import app as classify_intent
from app.api.chat.chat_routes import app as chat_routes

app = FastAPI()
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or a list of allowed origins, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods, e.g., GET, POST, PUT, DELETE
    allow_headers=["*"],  # Allows all headers
)

# Include the ai_routes router
app.include_router(ai_router)
app.include_router(data_routes)
app.include_router(auth_routes)
app.include_router(tenant_routes)
app.include_router(ecom_routes)
app.include_router(classify_intent)
app.include_router(chat_routes)

@app.get("/")
async def root():
    return {"message": "Welcome to the Intent API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
