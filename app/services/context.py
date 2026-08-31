
from app.services.retrieval import RetrievedChunk


class ContextBuilder:
    """Build LLM context from retrieved document chunks."""

    @staticmethod
    def build(
        results: list[RetrievedChunk],
    ) -> str:
        """Build a clean text-only context."""

        if not results:
            return ""

        sections: list[str] = []

        for index, result in enumerate(results, start=1):
            sections.append(
                f"[Source {index}]\n"
                f"{result.chunk.content.strip()}"
            )

        return "\n\n".join(sections)
