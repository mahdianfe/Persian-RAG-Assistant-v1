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
        """
        Remove model thinking blocks from Ollama output.
        Handles both complete and incomplete <think> blocks.
        """

        # حالت کامل:
        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        # حالت ناقص: فقط <think> آمده و پایان ندارد
        if "<think>" in text.lower():
            text = re.split(
                r"<think>",
                text,
                flags=re.IGNORECASE,
            )[0]
 
        return text.strip()    

    @staticmethod
    def _clean_answer(text: str) -> str:
        """
        Remove common answer wrappers added by LLM.
        """

        text = text.strip()

        # حذف بخش‌هایی که مدل خودش اضافه می‌کند
        patterns = [
            r"^###\s*توضیح:.*?(?=###|$)",
            r"^توضیح:.*?(?=\n\n|$)",
            r"^###\s*جواب نهایی:.*?\n",
            r"^جواب نهایی:\s*",
        ]

        for pattern in patterns:
            text = re.sub(
                pattern,
                "",
                text,
                flags=re.DOTALL,
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
                "think": False,
                "options": {
                    "temperature": 0.0,
                    "top_p": 0.01,
                    "top_k": 1,
                    "repeat_penalty": 1.2,
                    "num_predict": 128,
                },
            },
            timeout=180.0,
        )

        response.raise_for_status()

        data = response.json()

        content = data["response"]

        content = self._remove_thinking(content)

        content = self._clean_answer(content)

        return content
