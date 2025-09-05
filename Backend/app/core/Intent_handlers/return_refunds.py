def handle_return_request(order_db, entities):
    order_id = entities[0] if entities else None
    if order_id in order_db:
        return {"order_id": order_id, "status": "Return initiated"}
    return {"error": "Order not found"}

def handle_refund_status(order_db, entities):
    order_id = entities[0] if entities else None
    order = order_db.get(order_id)
    return {"order_id": order_id, "refund_status": order.get("refund_status", "Pending")} if order else {"error": "Order not found"}
