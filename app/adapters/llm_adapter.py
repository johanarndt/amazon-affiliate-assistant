# backend/app/adapters/llm_adapter.py

class LocalTemplateLLM:
    def __init__(self, *args, **kwargs):
        pass

    def generate(self, prompt: str) -> str:
        return "LLM disabled (placeholder response)"
