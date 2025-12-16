# app/llm.py
# Local LLM engine using GPT4All (no internet required)

import os
from gpt4all import GPT4All

# ------------------------------------------------------------
# Load a local GPT4All model
# ------------------------------------------------------------

# Directory where GPT4All stores downloaded models
MODEL_DIR = os.path.expanduser("~/.cache/gpt4all")

# You may replace this model name with ANY model you downloaded
DEFAULT_MODEL = "gpt4all-falcon-newbpe-q4_0.gguf"

# Ensure directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load the model
try:
    llm = GPT4All(
        DEFAULT_MODEL,
        model_path=MODEL_DIR,
        device="cpu"   # CPU only, works on every machine
    )
    MODEL_READY = True
except Exception as e:
    print("LLM loading failed:", e)
    llm = None
    MODEL_READY = False


# ------------------------------------------------------------
# Main engine function used by API
# ------------------------------------------------------------

def llm_engine(prompt: str) -> str:
    """
    Sends prompt to local GPT4All LLM.

    Returns a string reply,
    or a safe fallback string if the model is not available.
    """

    if not MODEL_READY or llm is None:
        return (
            "Local AI model is not available at the moment. "
            "Please confirm your GPT4All model file is correctly installed."
        )

    try:
        response = llm.generate(
            prompt,
            max_tokens=300,
            temp=0.7,
            top_k=40
        )
        return response.strip()
    except Exception as e:
        return f"LLM engine error: {e}"
