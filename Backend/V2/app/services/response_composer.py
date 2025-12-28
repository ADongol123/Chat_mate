from typing import Dict, Optional

class ResponseComposer:
    """
    Converts Decision Engine output into human-like, sales-grade responses.
    """

    def __init__(self):
        pass

    def compose(self, decision: Dict) -> str:
        """
        decision: {
            "response_text": str,
            "action": str,
            "data": dict (products, cart, etc.)
        }
        """

        action = decision.get("action")
        data = decision.get("data", {})
        base_text = decision.get("response_text", "")

        # Add product intelligence for search results
        if action == "search_product" and "products" in data:
            products = data["products"]
            if products:
                product_lines = []
                for p in products:
                    line = f"{p.get('name')} (${p.get('price')}, {p.get('rating')}★)"
                    product_lines.append(line)
                base_text += "\nHere are some options:\n" + "\n".join(product_lines)

        # Add reasoning for highest rated / cheapest
        elif action in ["get_highest_rated", "get_cheapest"] and "product" in data:
            p = data["product"]
            if action == "get_highest_rated":
                base_text += f"\nThis is the highest-rated product with {p.get('rating')}★ and costs ${p.get('price')}."
            elif action == "get_cheapest":
                base_text += f"\nThis is the cheapest product at ${p.get('price')} with {p.get('rating')}★ rating."

        # Add cart info
        elif action == "add_to_cart" and "product" in data:
            p = data["product"]
            base_text += f"\nI've added {p.get('name')} to your cart. Happy shopping!"

        # Clarification messages
        elif action == "clarify":
            base_text = f"{base_text} Can you provide more details?"

        return base_text
