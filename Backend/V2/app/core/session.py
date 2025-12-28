from typing import Dict
from datetime import datetime
from typing import Optional
from V2.app.db import db
SESSION_COLLECTION = "sessions"

class ConversationState:
    """
    State Management
    """
    
    def __init__(self, session_id: str, data:Optional[Dict]=None):
        self.session_id = session_id
        self.data = data or {}
        self.data.setdefault("created_at", datetime.utcnow())
        self.data.setdefault("last_updated", datetime.utcnow())
        
    
    def update_timestamp(self):
        self.data["last_updated"] = datetime.utcnow()
        
        
    
class SessionStore:
    @staticmethod
    async def get_or_create(session_id:  str) -> ConversationState:
        doc = await db[SESSION_COLLECTION].find_one({
            "session_id": session_id
        })
        if not doc:
            state = ConversationState(session_id)
            await db[SESSION_COLLECTION].insert_one({
                {"session_id": session_id, **state.data},
            })
            return state
        return ConversationState(session_id, data=doc)
    
    @staticmethod
    async def update(session: ConversationState):
        session.update_timestamp()
        await db[SESSION_COLLECTION].update_one(
            {"session_id": session.session_id},
            {"$set": session.data}, upsert=True
        )
        
    @staticmethod
    async def delete(session_id: str):
        await db[SESSION_COLLECTION].delete_one({"session_id": session_id})