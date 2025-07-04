import httpx
from typing import Any
from ..config import get_settings

LLAMA_ENDPOINT = "https://api.llama.ai/v1/chat/completions"  # à adapter selon doc officielle

async def generate_llama(
    prompt: str,
    *,
    model: str = "llama-3-70b-chat",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **extra: Any,
) -> str:
    settings = get_settings()

    headers = {
        "Authorization": f"Bearer {settings.LLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        **extra,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(LLAMA_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
