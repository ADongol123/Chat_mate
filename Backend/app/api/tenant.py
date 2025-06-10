from fastapi import APIRouter, Depends,  HTTPException
from app.schemas.tenant_schema import TenantCreate
from app.services.tenant_service import create_tenant, approve_tenant
from typing import Dict


app = APIRouter(prefix="/tenants", tags=["Tenants"])


@app.post("/")
async def create_tenant_route(data: TenantCreate):
    try:
        return await create_tenant(data)
    except Exception as e:
        raise HTTPException(status_code=400 , detail=str(e))



@app.post("approve/{tenant_id}")
async def approve_tenant_route(tenant_id:str):
    try:
        return await approve_tenant(tenant_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
