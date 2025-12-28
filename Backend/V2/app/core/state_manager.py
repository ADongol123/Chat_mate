from typing import Dict, Optional
from V2.app.core.session import SessionStore
from datetime import datetime
from V2.app.utils.logger import logger
class StateManager:
    """
    Production-grade conversation state manager
    Handles:
    - User prefrences
    - Cart & products discussed
    - Refrence resolution 
    - Confidence tracking
    """
    
    def __init__(self):
        pass
    
    async def get_state(self, session_id: str) -> Dict:
        """
        Returns the full conversation state from MongoDB
        """
        
        state = await SessionStore.get_or_create(session_id)
        return state.data
    
    
    async def update_prefrences(
        self,
        session_id: str,
        category: Optional[str] = None,
        budget: Optional[float] = None,
        priority: Optional[str] = None
    ):
        state = await SessionStore.get_or_create(session_id)
        if category:
            state.data["category"] = category
        if budget:
            state.data["budget"] = budget
        if priority:
            state.data["priority"] = priority
        
        
        state.data["last_updated"] = datetime.utcnow()
        await SessionStore.update(state)
        logger.info(f"Updated prefrences for session {session_id}")
        
    async def add_product_show(self, sessison_id:str, product:Dict):
        state = await SessionStore.get_or_create(sessison_id)
        if "products_shown" not in state.data:
            state.data["products_shown"] = []
        state.data["products_shown"].append(product)
        state.data["last_referenced_product"] = product
        state.data["last_updated"] = datetime.utcnow()
        await SessionStore.update(state)
        logger.info(f"Added product to shown list for session {sessison_id}: {product.get('name')}")
        
    async def add_to_cart(self, session_id: str, product: Dict):
        """
        Adds the last referenced product to the cart with confidence level
        """
        state = await SessionStore.get_or_create(session_id)
        if  "cart" not in state.data:
            state.data["cart"] = []
        state.data["cart"].append(product)
        state.data["last_updated"] = datetime.utcnow()
        await SessionStore.update(state)
        logger.info(f"Added product to cart for session {session_id}: {product.get('name')}")
        
    async def update_confidence(self, session_id:str, confidence:str):
        """
        Confidence can be low | medium | high
        """
        state = await SessionStore.get_or_create(session_id)
        state.data["confidence_level"] = confidence
        state.data["last_updated"] = datetime.utcnow()
        await SessionStore.update(state)
        logger.info(f"Updated confidence level for session {session_id} to {confidence}")
        
        
    async def resolve_reference(self, session_id: str, text:str) -> Optional[Dict]:
        """
        Resolve refrences like "this one", "that one", "previous"
        """
        reference_terms = ["this", "that", "this one", "that one", "previous"] 
        state =await SessionStore.get_or_create(session_id)
        
        if any(term in text.lower() for term in reference_terms):
            return state.data.get("last_referenced_product")
        
        return None