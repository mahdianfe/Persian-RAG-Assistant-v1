import re

import httpx

from app.core.config import settings
from app.llm.service import LLMService


class OllamaLLMService(LLMService):
    """LLM provider backed by Ollama."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        self.base_url = (
            base_url or settings.ollama_base_url
        ).rstrip("/")

        self.model = model or settings.llm_model

    @staticmethod
    def _remove_thinking(text: str) -> str:
        """Remove model thinking blocks from the final answer."""

        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        return text.strip()

    def generate(self, prompt: str) -> str:
        """Generate a response using Ollama generate API."""

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "top_p": 0.8,
                },
            },
            timeout=180.0,
        )

        response.raise_for_status()

        data = response.json()

        content = data["response"]

        return self._remove_thinking(content)
