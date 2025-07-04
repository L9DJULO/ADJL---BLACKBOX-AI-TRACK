import httpx
from ..config import get_settings

GROKCLOUD_ENDPOINT  = "https://api.groq.com/openai/v1/chat/completions"

async def query_groqcloud(prompt: str) -> str:
    settings = get_settings()

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GROKCLOUD_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()

    data = response.json()
    return data["choices"][0]["message"]["content"]
