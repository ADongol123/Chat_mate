from app.schemas.user_schema import UserCreate
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.db.database import db
from bson import ObjectId
from app.schemas.user_schema import UserRole,AccountType

async def register_user(data):
    print(data, "data")

    # 1. Check if user already exists 
    user = await db.users.find_one({"email": data.email})
    if user:
        raise Exception("User already exists")

    # Check account type and set has_paid accordingly
    if data.account_type == AccountType.PAID:
        has_paid = False  # Initially, a paid tenant hasn't completed the payment yet
    elif data.account_type == AccountType.FREE:
        has_paid = False  # A free tenant has access without payment

    # Register the tenant user with account type
    new_user = UserCreate(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role,  # Assuming role is passed in the data
        account_type=data.account_type,
        has_paid=has_paid,  # Set payment status
    )

    # Insert the new tenant user into the database
    await db.users.insert_one(new_user.dict())
    return {"msg": "Tenant Registered Successfully"}




async def login_user(data):
    user = await db.users.find_one({"email": data.email})
    
    if not user:
        raise Exception("Invalid Credentials")
    
    if not verify_password(data.password, user['password']):
        raise Exception("Invalid Credentials")
    
    # Check if account is paid or free and validate payment status for paid accounts
    if user["account_type"] == AccountType.PAID:
        if not user.get("has_paid", False):
            raise Exception("Payment required for paid account. Please complete payment to login.")
    
    
    # if user["role"] == UserRole.ADMIN:
    #     tenant_id = user.get('tenant_id')
    #     if tenant_id:
    #         tenant = await db.tenants.find_one({"id": ObjectId(tenant_id)})
    #         if not tenant:
    #             raise Exception("Tenant not found")
    #         if tenant['status'] != "approved":
    #             raise Exception("Tenant is not approved yet")
            
    if user.get("account_type") == "paid" and not user.get("has_paid", False):
        raise Exception("Payment required for paid account. Please compelte payment to login ")
    
    # Create token
    token_data = {
        "user_id" : str(user["_id"]),
        "email" : user["email"],
        "role" : user["role"],
        "account_type": user.get("account_type"),
    }
    
    token = create_access_token(token_data)
    return {"access_token": token}