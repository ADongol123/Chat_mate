from datetime import datetime 
from bson import ObjectId
import os 
from app.db.database import db

async def create_tenant(data):
    existing  = await db.tenants.find_one({"name":data.name})
    if existing:
        raise Exception("Tenannt with this name already exitst")
    
    new_teant = {
        "name": data.name,
        "email": data.contact_email,
        "domain": data.domain,
        "description": data.description,
        "created_at": datetime.utcnow(),
        "status" : "pending"
    }
    
    print(new_teant,"new_tenanat")
    await db.tenants.insert_one(new_teant)
    return{"message": "Tenant created Successfully"}




async def approve_tenant(tenant_id:str):
    result = await db.tenants.update_one(
        {"_id":ObjectId(tenant_id)},
        {"$set":{"status":"approved"}}
    )
    
    if result.modified_count == 0:
        raise Exception("Tenant not found or already approved")
    
    return {"msg" : "Tenant approved successfully"}



