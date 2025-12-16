from fastapi import APIRouter
from pydantic import BaseModel
from app.services import llm_engine

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    prompt: str

@router.post("/")
def chat(req: ChatRequest):
    response = llm_engine.chat(req.prompt)
    return {"response": response}

