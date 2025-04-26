from app.db.database import db
from app.schemas.user_schema import UserCreate
import hashlib
from datetime import datetime


async def create_user(user: UserCreate):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    user_data = user.dict()
    user_data['password'] = hashed_pw
    user_data['created_at'] = datetime.utcnow()
    user_data['updated_at'] = datetime.utcnow()
    result = await db["users"].insert_one(user_data)
    user_data["_id"] = str(result.inserted_id)
    return user_data



