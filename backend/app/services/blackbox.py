import httpx
from typing import Any
from ..config import get_settings
import requests
import json

BLACKBOX_ENDPOINT = "https://api.blackbox.ai/chat/completions"  # à adapter selon doc officielle
user_api_key = 'sk-GIldanA_IAnQQq86orMwdg'

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {user_api_key}"
}

data = {
    "model": "blackboxai/openai/gpt-4",
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
}

response = requests.post(BLACKBOX_ENDPOINT, headers=headers, json=data)
print(response.json())
