from V2.app.models.intent import Intent
from V2.app.llm.base import BaseLLM

class IntentExtractor:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def extract(self, user_text: str) -> Intent:
        result = await self.llm.extract_intent(user_text)
        intent_name = result.get("intent", "unknown")
        confidence = result.get("confidence", 0.0)
        slots = result.get("slots", {})
        return Intent(name=intent_name, confidence=confidence, slots=slots)
