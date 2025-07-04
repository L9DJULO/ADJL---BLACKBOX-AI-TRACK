from pydantic import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    GROQCLOUD_API_KEY: str
    LLAMA_API_KEY: str
    BLACKBOX_API_KEY: str

    class Config:
        env_file = Path(__file__).resolve().parents[1] / ".env"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()
