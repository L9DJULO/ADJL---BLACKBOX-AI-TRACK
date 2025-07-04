from fastapi import APIRouter
from pydantic import BaseModel
from ..services.blackbox import blackbox_completion

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_blackbox(req: PromptRequest):
    """
    Appelle BlackBox.ia avec le prompt fourni et renvoie la réponse.
    """
    response = await blackbox_completion(req.prompt)
    return {"response": response}
