import os
import json
import re
import httpx
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL     = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL   = "mistral-small-latest"


def ask_mistral(system_prompt: str, user_message: str) -> str:
    """
    Send a message to Mistral AI and get a text reply back.
    
    system_prompt: Instructions telling Mistral how to behave
    user_message:  The actual question or task
    
    Returns: Mistral's text answer as a string
    """
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY not found in .env file")

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        "temperature": 0.1   # Low = more consistent, factual answers
    }

    response = httpx.post(
        MISTRAL_URL,
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_json_from_mistral(text: str) -> dict:
    """
    Mistral sometimes wraps JSON in markdown code fences like ```json ... ```
    This function strips that and returns clean Python dict.
    
    Use this when you need Mistral to return structured data (e.g. invoice fields).
    """
    cleaned = re.sub(r"```json|```", "", text).strip()
    return json.loads(cleaned)

# NOTE: You need a Mistral API key. Get one at console.mistral.ai and add to .env
