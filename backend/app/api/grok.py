from fastapi import APIRouter
from pydantic import BaseModel
from ..services.grokcloud import query_grokcloud

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_grok(req: PromptRequest):
    """
    Appelle GrokCloud avec le prompt fourni et renvoie la réponse.
    """
    response = await query_grokcloud(req.prompt)
    return {"response": response}