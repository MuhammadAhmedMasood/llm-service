import time
from typing import Dict, Any
from openai import OpenAI
from core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


class ModelRouter:
    def __init__(self):
        # You can later extend this with Anthropic / Local models
        self.rules = {
            "classify": "gpt-3.5-turbo",
            "summarise": "gpt-3.5-turbo",
            "generate": "gpt-4-turbo",
        }

    def select_model(self, task: str, mode: str) -> str:
        return self.rules.get(task, settings.default_model)

    def call_model(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 300
    ) -> Dict[str, Any]:
        start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        end = time.time()

        message = response.choices[0].message.content
        usage = response.usage

        return {
            "output": message,
            "tokens_used": usage.total_tokens,
            "latency_ms": round((end - start) * 1000, 2),
            "model": model
        }
