from app.models.chat import ChatRequest, ChatResponse, generate_response



app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok", "message": "Backend running (Groq enabled)"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return generate_response(req.text)



    







