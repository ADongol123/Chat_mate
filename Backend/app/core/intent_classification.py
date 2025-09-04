from typing import Dict, Any
from textblob import TextBlob
from app.utils.ecom_helpers import clean_llm_json, load_prompt
import ollama
from tenacity import retry, stop_after_attempt, wait_exponential
import langdetect

class ClassificationError(Exception):
    pass

def load_classification_prompt(template_path: str, query: str) -> str:
    """
    Load intent classification prompt template and inject the query.
    """
    with open(template_path, "r") as f:
        template = f.read()
    # Replace placeholder {query} in your prompt
    return template.replace("{query}", query)



def classify_intent_with_mistral(query: str) -> Dict[str, Any]:
    """
    Classify query using Mistral LLM. Return JSON with intent, entities and confidence.
    """
    
    if not query or query.isspace():
        return {"intent": "unknown", "key_entities": [], "confidence": 1.0}
    
    
    # Preprocess query
    query = query.lower().strip()
    
    query = str(TextBlob(query).correct())
    
    # Detect non-English
    is_non_english = False
    
    try:
        if langdetect.detect(query) != "en":
            is_non_english = True
    except:
        pass
    
    
    # Load prompt
    prompt = load_classification_prompt("app/prompt/intent_classification.txt", query)

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}],
            options = {"temperature": 0.3}
        )  
        raw_output = response["message"]["content"]
        print("Raw output from Mistral:", raw_output)
    except Exception as e:
        raise ClassificationError(f"Mistral API error: {str(e)}")
    
    
    result  = clean_llm_json(raw_output)
    print("Cleaned output:", result)
    return result