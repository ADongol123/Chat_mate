from typing import Dict, Optional
from V2.app.core.state_manager import StateManager
from V2.app.models.intent import Intent
from V2.app.utils.logger import logger
from V2.app.services.qdrant_client import ProductRetriever
from V2.app.llm.embedding_client import EmbeddingClient
from datetime import datetime

class DecisionEngine:
    """
    Maps intent + slots + state → actions
    Production-grade engine: easily extendable for multiple actions.
    """

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.product_retriever = ProductRetriever()
        self.embedding_client = " "
    async def handle_intent(self, session_id: str, intent: Intent) -> Dict:
        """
        Main entry point.
        Returns a dict:
        {
            "response_text": str,
            "action": Optional[str],   # search, add_to_cart, compare, clarify
            "data": Optional[dict]     # additional info like products, cart, etc.
        }
        """
        # Get current session state
        state = await self.state_manager.get_state(session_id)

        # If confidence is low, ask clarification
        if intent.confidence < 0.6:
            return {
                "response_text": "I’m not sure I understood that. Could you clarify?",
                "action": "clarify",
                "data": None
            }

        # Map intents
        if intent.name == "search_product":
            category = intent.slots.get("category")
            price = intent.slots.get("price")
            # Update state preferences
            if category or price:
                await self.state_manager.update_preferences(session_id, category=category, priority=price)

            # Action: retrieve products (dummy for now, real retrieval in Step 6)
            products = await self._mock_retrieve_products(category, price)
            # Update state with products shown
            for product in products:
                await self.state_manager.add_product_shown(session_id, product)

            return {
                "response_text": f"I found {len(products)} products for you in {category or 'any category'}.",
                "action": "search_product",
                "data": {"products": products}
            }

        elif intent.name == "add_to_cart":
            last_product = state.get("last_referenced_product")
            if last_product:
                await self.state_manager.add_to_cart(session_id, last_product)
                return {
                    "response_text": f"Added {last_product.get('name')} to your cart.",
                    "action": "add_to_cart",
                    "data": {"product": last_product}
                }
            else:
                return {
                    "response_text": "I couldn’t find the product you want to add. Can you specify?",
                    "action": "clarify",
                    "data": None
                }

        elif intent.name == "get_highest_rated":
            products = state.get("products_shown", [])
            if products:
                product = max(products, key=lambda x: x.get("rating", 0))
                return {
                    "response_text": f"The highest rated product is {product.get('name')} with {product.get('rating')} stars.",
                    "action": "get_highest_rated",
                    "data": {"product": product}
                }
            else:
                return {
                    "response_text": "I have not shown any products yet. Please search first.",
                    "action": "clarify",
                    "data": None
                }

        elif intent.name == "get_cheapest":
            products = state.get("products_shown", [])
            if products:
                product = min(products, key=lambda x: x.get("price", float('inf')))
                return {
                    "response_text": f"The cheapest product is {product.get('name')} at ${product.get('price')}.",
                    "action": "get_cheapest",
                    "data": {"product": product}
                }
            else:
                return {
                    "response_text": "I have not shown any products yet. Please search first.",
                    "action": "clarify",
                    "data": None
                }

        else:
            return {
                "response_text": "I understood your message, but I can't handle this action yet.",
                "action": "unknown",
                "data": None
            }

    async def _mock_retrieve_products(self, category: Optional[str], price: Optional[str]):
        """
        Temporary dummy product retrieval.
        In Step 6, replace with Qdrant vector search or database query.
        """
        mock_products = [
            {"name": f"{category or 'Product'} A", "price": 50, "rating": 4.2},
            {"name": f"{category or 'Product'} B", "price": 30, "rating": 4.5},
            {"name": f"{category or 'Product'} C", "price": 70, "rating": 3.9}
        ]
        if price == "cheap":
            return sorted(mock_products, key=lambda x: x["price"])[:2]
        elif price == "expensive":
            return sorted(mock_products, key=lambda x: x["price"], reverse=True)[:2]
        return mock_products
