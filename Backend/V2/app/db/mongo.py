from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import logger
from app.utils.config import settings

MONGO_URI = settings.MONGODB_URL
DB_NAME = "ChatmateV2"


client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


logger.info("Connected to MongoDB database: %s", DB_NAME)