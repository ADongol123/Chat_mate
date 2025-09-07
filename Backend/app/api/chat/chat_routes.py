from fastapi import APIRouter,Depends, HTTPException
from app.api.chat.chat_models import Chatbot,ChatbotCreate,ChatBotBase
from app.utils.jwt_handler import get_current_user
from datetime import datetime
from typing import List
from bson import ObjectId
from app.db.collection import chatbots_collection

app = APIRouter(prefix="/chatbots",tags=['Chatbots'])


# -------------------------------------------------------------
# Create Chatbot
# ----------------------------------------------------------------
@app.post("/",response_model=Chatbot)
async def create_chatbot(payload:ChatbotCreate, user = Depends(get_current_user)):
    chatbot = payload.dict()
    chatbot['user_email'] = user['email']
    chatbot['created_at'] = datetime.utcnow()
    chatbot['updated_at'] = datetime.utcnow()
    
    result = await chatbots_collection.insert_one(chatbot)
    chatbot["id"] = result.inserted_id
    return chatbot



# -------------------------------------------------------------
# Get all Chatbots
# ----------------------------------------------------------------
@app.get("/", response_model=List[Chatbot])
async def get_chatbots(chatbot_id: str, user=Depends(get_current_user)):
    chatbot = await chatbots_collection.find_one({"_id": ObjectId(chatbot_id), "user_email":user['email']})
    if not chatbot:
        return []

    chatbot["id"] = str(chatbot["_id"])
    
    return [chatbot]


#-----------------------------------------------------
# Get chatbot by id
#-----------------------------------------------------

@app.get("/{chatbot_id}", response_model = Chatbot)
async def get_chatbot(chatbot_id:str, user = Depends(get_current_user)):
    chatbot = await chatbots_collection.find_one({"_id":ObjectId(chatbot_id), "user_email": user["email"]})
    if not chatbot:
        raise HTTPException(status_code = 404, details= "Chatbot not found")
    
    
    chatbot["id"] = chatbot["_id"]
    return chatbot



#------------------------------------------------------
# Update Chatbot
# ---------------------------------------------------
@app.put("/{chatbot_id}", response_model=Chatbot)
async def update_chatbot(chatbot_id: str, payload: ChatBotBase, user=Depends(get_current_user)):
    chatbot = await chatbots_collection.find_one({"_id": ObjectId(chatbot_id), "user_email": user["email"]})
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")

    update_data = payload.dict()
    update_data["updated_at"] = datetime.utcnow()

    await chatbots_collection.update_one(
        {"_id": ObjectId(chatbot_id)},
        {"$set": update_data}
    )

    chatbot.update(update_data)
    chatbot["id"] = chatbot["_id"]
    return chatbot


#------------------------------------------------------------
# Delete Chatbot
#-----------------------------------------------------------------
@app.delete("/{chatbot}")
async def delete_chatbot(chatbot_id: str, user = Depends(get_current_user)):
    results = await chatbots_collection.delete_one({"_id":ObjectId(chatbot_id), "user_email":user["email"]})
    if results.delete_count == 0:
        raise HTTPException(status_code=404, details = "Chatbot bot found")
    
    return {"message": "Chatbot delted successfully"}


#-----------------------------------------------------------------------------
# Deploy chatbot {generate snippet}
# -----------------------------------------------------------------------------
@app.get("/{chabot_id}/deploy")
async def deploy_model(chatbot_id: str, user= Depends(get_current_user)):
    chatbot = await chatbots_collection.find_one({"_id":ObjectId(chatbot_id), "user_email":user["email"]})
    if not chatbot:
        raise HTTPException(status_code=404, detail = "Chatbot not found")
    
    script = f"""
    <script>
      (function(d,s,id){{
        var js,fjs=d.getElementsByTagName(s)[0];
        if(d.getElementById(id))return;
        js=d.createElement(s);js.id=id;
        js.src="https://chatbotsaas.com/embed.js";
        js.setAttribute('data-chatbot-id','{str(chatbot["_id"])}');
        fjs.parentNode.insertBefore(js,fjs);
      }})(document,'script','chatbot-embed');
    </script>
    """
    return {"embed_code": script}



