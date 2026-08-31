from abc import ABC, abstractmethod


class LLMService(ABC):
    """Interface for large language model providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response from a prompt."""
        raise NotImplementedError
