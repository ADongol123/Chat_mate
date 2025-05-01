from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("DB_NAME")
MONGO_COMPANY_DATA_COLLECTION = os.getenv("COMPANY_DATA_COLLECTION")

client  = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
company_data_collection = db[MONGO_COMPANY_DATA_COLLECTION]