from fastapi import APIRouter

router = APIRouter()

# Import routers defined in sibling modules
from . import grok, llama, blackbox  # noqa: E402

# Mount sub‑routers with path prefixes
router.include_router(grok.router, prefix="/grok", tags=["GrokCloud"])
router.include_router(llama.router, prefix="/llama", tags=["Llama"])
router.include_router(blackbox.router, prefix="/blackbox", tags=["BlackBox"])

__all__ = ["router"]