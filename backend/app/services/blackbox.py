import httpx
from typing import Any
from ..config import get_settings

BLACKBOX_ENDPOINT = "https://api.blackbox.ai/v1/completions"  # à adapter selon doc officielle

async def blackbox_completion(
    prompt: str,
    *,
    model: str = "blackbox-embed-large",
    temperature: float = 0.7,
    max_tokens: int = 512,
    **extra: Any,
) -> str:
    settings = get_settings()

    headers = {
        "Authorization": f"Bearer {settings.BLACKBOX_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        **extra,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(BLACKBOX_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

    data = response.json()
    return data["choices"][0]["text"].strip()
