from app.utils.ecom_helpers import clean_llm_json, load_prompt
import ollama

def rerank_with_mistral(intent: str, query: str, candidates: list, k: int = 5):
    """
    Rerank candidates using Mistral with intent-specific prompts.
    - intent: 'discount', 'search', or others
    - query: user query
    - candidates: list of tuples (doc, score)
    - k: max number of results
    """
    # Prepare candidate text
    docs_text = "\n\n".join(
        [f"Doc {i+1}: {doc.page_content}\nMetadata: {doc.metadata}" 
         for i, (doc, score) in enumerate(candidates)]
    )

    # Select prompt based on intent
    if intent.lower() == "discount":
        prompt_template_path = "app/prompt/rerank_discount_prompt_prod.txt"
    else:
        prompt_template_path = "app/prompt/rerank_prompt.txt"  # generic search

    # Load and fill prompt
    prompt = load_prompt(prompt_template_path, query, docs_text, k=k)

    # Call Mistral
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]
    parsed_output = clean_llm_json(raw_output)

    # Optional: filter for discount if intent is discount
    if intent.lower() == "discount":
        parsed_output = [
            doc for doc in parsed_output if doc.get("discount_percentage", 0) > 0
        ]

    # Limit results to k
    return parsed_output[:k]
