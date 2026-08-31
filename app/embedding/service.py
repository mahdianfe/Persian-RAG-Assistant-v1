from abc import ABC, abstractmethod


class EmbeddingService(ABC):
    """Interface for text embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Create an embedding vector for one text."""
        raise NotImplementedError

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Create embeddings for multiple texts."""

        return [self.embed(text) for text in texts]
