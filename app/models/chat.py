from pydantic import BaseModel
from groq import Groq
import os


class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


def generate_response(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=256,
    )

    return completion.choices[0].message.content

