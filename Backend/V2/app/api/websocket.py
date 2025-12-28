from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

from V2.app.core.state_manager import StateManager
from V2.app.models.message import BotMessage
from V2.app.utils.logger import logger
from V2.app.llm.llama_client import OpenAILLM
from V2.app.services.intent_extractor import IntentExtractor
from V2.app.core.decision_engine import DecisionEngine
from V2.app.services.response_composer import ResponseComposer
# Initialize
router = APIRouter()
state_manager = StateManager()
llm_client = OpenAILLM()
intent_extractor = IntentExtractor(llm_client)
decision_engine = DecisionEngine(state_manager)
response_composer = ResponseComposer()

@router.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        while True:
            data = await websocket.receive_json()
            session_id = data.get("session_id")
            user_text = data.get("message")

            if not session_id or not user_text:
                await websocket.send_json({"error": "session_id and message required"})
                continue

            # 1️⃣ Extract intent and slots
            intent = await intent_extractor.extract(user_text)

            # 2️⃣ Execute Decision Engine (Step 4 core)
            decision = await decision_engine.handle_intent(session_id, intent)

            response_text = response_composer.compose(decision)
            

            # 4️⃣ Send structured response to client
            response = BotMessage(
                session_id=session_id,
                message=response_text,
                timestamp=datetime.utcnow()
            )
            await websocket.send_json(response.dict())

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
