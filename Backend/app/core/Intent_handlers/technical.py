def handle_technical_issue(entities):
    return {"issue": " ".join(entities), "status": "Reported to technical team"}

def handle_app_support(entities):
    return {"issue": " ".join(entities), "status": "Escalated to mobile app team"}
