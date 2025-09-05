def handle_product_search(df, entities):
    query = " ".join(entities).lower()
    results = df[df["product_name"].str.lower().str.contains(query, na=False)]
    return results[["product_name", "price"]].to_dict(orient="records") if not results.empty else {"error": "No products found"}

def handle_product_comparison(df, entities):
    results = df[df["product_name"].str.lower().str.contains("|".join(entities), na=False)]
    return results[["product_name", "price", "rating"]].to_dict(orient="records") if not results.empty else {"error": "Products not found"}

def handle_product_recommendation(df, entities):
    # naive recommendation → filter by keyword and return top 5 by rating
    query = " ".join(entities).lower()
    results = df[df["description"].str.lower().str.contains(query, na=False)].sort_values(by="rating", ascending=False)
    return results.head(5)[["product_name", "price", "rating"]].to_dict(orient="records")

def handle_product_availability(df, entities):
    query = " ".join(entities).lower()
    match = df[df["product_name"].str.lower().str.contains(query, na=False)]
    return {"product": match.iloc[0]["product_name"], "availability": match.iloc[0]["availability"]} if not match.empty else {"error": "Product not found"}

def handle_product_details(df, entities):
    query = " ".join(entities).lower()
    match = df[df["product_name"].str.lower().str.contains(query, na=False)]
    return match.iloc[0].to_dict() if not match.empty else {"error": "Product not found"}
