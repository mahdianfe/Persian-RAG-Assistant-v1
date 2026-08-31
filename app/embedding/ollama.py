import httpx

from app.core.config import settings
from app.embedding.service import EmbeddingService


class OllamaEmbeddingService(EmbeddingService):
    """Embedding provider backed by Ollama."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        self.base_url = (
            base_url or settings.ollama_base_url
        ).rstrip("/")

        self.model = model or settings.embedding_model

    def embed(self, text: str) -> list[float]:
        """Create an embedding for one text."""

        response = httpx.post(
            f"{self.base_url}/api/embed",
            json={
                "model": self.model,
                "input": text,
            },
            timeout=120.0,
        )

        response.raise_for_status()

        data = response.json()

        embeddings = data["embeddings"]

        if not embeddings:
            raise ValueError("Ollama returned no embeddings.")

        vector = embeddings[0]

        if len(vector) != 1024:
            raise ValueError(
                f"Expected 1024 dimensions, got {len(vector)}."
            )

        return vector
