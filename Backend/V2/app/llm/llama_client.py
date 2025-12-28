import os
import openai
from V2.app.llm.base import BaseLLM

openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenAILLM(BaseLLM):
    async def extract_intent(self, text: str):
        prompt = f"""
        Extract intent and slots from the user message.
        Output JSON with keys: intent, confidence (0-1), slots (category, price, rating)
        User message: "{text}"
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Extract JSON from response
        content = response.choices[0].message.content
        import json
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"intent": "unknown", "confidence": 0.0, "slots": {}}
