def handle_order_tracking(order_db, entities):
    order_id = entities[0] if entities else None
    order = order_db.get(order_id)
    return {"order_id": order_id, "status": order["status"]} if order else {"error": "Order not found"}

def handle_order_modification(order_db, entities):
    order_id = entities[0] if entities else None
    if order_id in order_db:
        order_db[order_id]["status"] = "Cancelled"
        return {"order_id": order_id, "message": "Order cancelled successfully"}
    return {"error": "Order not found"}

def handle_order_issue(order_db, entities):
    return {"issue_reported": " ".join(entities), "status": "Escalated to support"}

def handle_delivery_inquiry(order_db, entities):
    order_id = entities[0] if entities else None
    order = order_db.get(order_id)
    return {"order_id": order_id, "estimated_delivery": order["estimated_delivery"]} if order else {"error": "Delivery info not found"}
