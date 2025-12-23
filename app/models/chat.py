from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str | None = None
    message: str | None = None

    @property
    def text(self) -> str:
        return self.prompt or self.message or ""




