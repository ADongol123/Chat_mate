def handle_account_creation():
    return {"message": "You can create an account at /signup"}

def handle_account_login():
    return {"message": "Login available at /login"}

def handle_account_update(entities):
    return {"update": " ".join(entities), "status": "Profile updated"}
