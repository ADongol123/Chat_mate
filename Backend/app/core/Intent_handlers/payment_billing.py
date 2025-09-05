def handle_payment_methods():
    return {"payment_methods": ["Credit Card", "Debit Card", "PayPal", "Gift Card"]}

def handle_billing_issue(entities):
    return {"issue": " ".join(entities), "status": "Escalated to billing support"}

def handle_invoice_request(order_db, entities):
    order_id = entities[0] if entities else None
    order = order_db.get(order_id)
    return {"order_id": order_id, "invoice": order.get("invoice_url")} if order else {"error": "Invoice not found"}
