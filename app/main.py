from app.models.chat import ChatRequest, generate_response


app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok", "message": "Backend running (Groq enabled)"}


@app.post("/chat")
async def chat(req: ChatRequest):
    response = generate_response(req.text)
    return {"response": response}


    







