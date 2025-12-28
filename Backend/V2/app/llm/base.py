from abc import ABC, abstractmethod
from typing import Dict

class BaseLLM(ABC):
    @abstractmethod
    async def extract_intent(self, text: str) -> Dict:
        """
        Given user text, returns:
        {
            "intent": "search_product",
            "confidence": 0.95,
            "slots": {"category": "headphones", "price": "cheap"}
        }
        """
        pass
