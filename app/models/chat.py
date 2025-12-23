from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    prompt: Optional[str] = None
    message: Optional[str] = None

    @property
    def text(self) -> str:
        if self.prompt:
            return self.prompt
        if self.message:
            return self.message
        raise ValueError("Either 'prompt' or 'message' must be provided")


class ChatResponse(BaseModel):
    response: str


def generate_response(text: str) -> str:
    # This function should call Groq via your adapter
    # Placeholder safety return
    return text



