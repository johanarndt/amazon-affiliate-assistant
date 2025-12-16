from fastapi import APIRouter
from pydantic import BaseModel
from app.adapters.llm import get_llm_response

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest):
    reply = get_llm_response(request.message)
    return {"reply": reply}
