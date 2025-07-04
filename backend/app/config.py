from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
import os

env_file = Path(__file__).resolve().parents[1] / ".env"
if env_file.exists():
    load_dotenv(env_file)

class Settings:
    GROKCLOUD_API_KEY: str = os.environ["GROKCLOUD_API_KEY"]
    LLAMA_API_KEY: str = os.environ["LLAMA_API_KEY"]
    BLACKBOX_API_KEY: str = os.environ["BLACKBOX_API_KEY"]

@lru_cache
def get_settings() -> Settings:     
    return Settings()
