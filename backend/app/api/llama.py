from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llama import generate_llama

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_llama(req: PromptRequest):
    """
    Appelle Llama Models avec le prompt fourni et renvoie la réponse.
    """
    response = await generate_llama(req.prompt)
    return {"response": response}