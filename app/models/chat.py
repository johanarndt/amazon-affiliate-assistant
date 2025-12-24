from pydantic import BaseModel
from app.llm import groq_chat  # or whatever your Groq function is named


class ChatRequest(BaseModel):
    prompt: str | None = None
    message: str | None = None

    @property
    def text(self) -> str:
        return self.prompt or self.message or ""


class ChatResponse(BaseModel):
    response: str


def generate_response(text: str) -> ChatResponse:
    reply = groq_chat(text)
    return ChatResponse(response=reply)





