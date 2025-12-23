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


