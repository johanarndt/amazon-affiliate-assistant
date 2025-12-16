# translator.py
# GPT4All wrapper for translation/paraphrase tasks.
import os
import time
from typing import Optional

# Try to import GPT4All. If not available, translator will be a no-op fallback.
try:
    from gpt4all import GPT4All
    GPT4ALL_AVAILABLE = True
except Exception:
    GPT4ALL_AVAILABLE = False

MODEL_PATH = os.getenv("GPT4ALL_MODEL_PATH", "models/gpt4all-falcon-q4_0.gguf")
_MODEL = None

def _load_model():
    global _MODEL
    if _MODEL is None and GPT4ALL_AVAILABLE:
        try:
            _MODEL = GPT4All(MODEL_PATH)
        except Exception as e:
            print("GPT4All load error:", e)
            _MODEL = None
    return _MODEL

def translate_text(text: str, target_lang: str, max_tokens: int = 512) -> str:
    """
    Translate or rewrite `text` into target_lang.
    If GPT4All is not available, returns the source text.
    target_lang uses ISO two-letter codes (en, pt, de, fr, es, it, ja, nl, ar, etc.)
    """
    if not text:
        return text
    if target_lang in ("en", "EN", "eng"):
        return text

    model = _load_model()
    if model is None:
        # fallback: return original text (still ok)
        return text

    # Craft a short prompt that asks for natural-sounding translation.
    prompt = (
        f"Translate the following text into {target_lang} preserving meaning and natural marketing tone. "
        f"Keep short paragraphs and preserve bullet points if present.\n\n"
        f"Text:\n{text}\n\nTranslation:"
    )

    try:
        # Some gpt4all versions have .generate(prompt) or .generate(prompt, max_tokens=int)
        resp = model.generate(prompt, max_tokens=max_tokens)
        # If model returns a list or object, normalize to string:
        if isinstance(resp, (list, tuple)):
            resp = " ".join(str(r) for r in resp)
        return str(resp).strip()
    except Exception as e:
        print("translate_text error:", e)
        return text
