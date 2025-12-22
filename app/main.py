from fastapi import FastAPI, HTTPException
from app.models.chat import ChatRequest, ChatResponse, generate_response

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok", "message": "Backend running (Groq enabled)"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        output = generate_response(request.prompt)
        return ChatResponse(response=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))







