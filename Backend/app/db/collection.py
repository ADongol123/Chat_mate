
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from app.utils.config import settings


load_dotenv()


client  = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]

chatbots_collection = db["chat_details"]
embeddings_collection = db["embeddings"]