from fastapi import FastAPI, HTTPException
from app.services import llm_engine
from app.models.chat import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        reply = llm_engine.generate(payload.prompt)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






