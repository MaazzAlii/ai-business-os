from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai")
DEFAULT_MODEL = os.getenv("MISTRAL_MODEL", "mistral-7b-instruct")


def _extract_text(response_data: dict[str, Any]) -> str:
    if response_data is None:
        return ""

    if isinstance(response_data.get("output"), str):
        return response_data["output"]

    if isinstance(response_data.get("output"), list):
        return "".join(str(item) for item in response_data["output"])

    results = response_data.get("results")
    if isinstance(results, list):
        text_parts: list[str] = []
        for result in results:
            content = result.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "output_text":
                        text_parts.append(str(block.get("text", "")))
        if text_parts:
            return "".join(text_parts)

    if isinstance(response_data.get("completion"), str):
        return response_data["completion"]

    return str(response_data)


async def ask_mistral_question(question: str) -> str:
    if not MISTRAL_API_KEY:
        return (
            "Mistral API key is not configured. "
            "Set MISTRAL_API_KEY in backend/.env or backend/.env.example."
        )

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEFAULT_MODEL,
        "input": question,
        "temperature": 0.6,
        "max_tokens": 512,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(f"{MISTRAL_API_URL}/v1/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    return _extract_text(data)
