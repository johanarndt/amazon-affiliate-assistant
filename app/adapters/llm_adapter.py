
from gpt4all import GPT4All

class LocalTemplateLLM:
    def __init__(self):
        model_filename = "mistral-7b-instruct-v0.1.Q4_0.gguf"
        model_path = "C:/Users/jarnd/Downloads/amazon-affiliate-assistant/backend/models"
        self.model = GPT4All(model_filename, model_path=model_path)

    def chat(self, prompt: str) -> str:
        return self.model.generate(prompt, max_tokens=200)
