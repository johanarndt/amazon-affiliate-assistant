from fastapi import FastAPI
from app.services import llm_engine

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok", "message": "Backend running (Groq enabled)"}

@app.post("/chat")
def chat(prompt: str):
    return {"response": llm_engine.generate(prompt)}





