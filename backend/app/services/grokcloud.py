import httpx
from ..config import get_settings

async def query_grokcloud(prompt: str) -> str:
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.GROKCLOUD_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"prompt": prompt}

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post("https://api.grokcloud.io/v1/chat", json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
