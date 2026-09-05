from unittest.mock import Mock

from app.services.context import ContextBuilder
from app.services.prompt import RAGPrompt


def make_retrieved_chunk(content: str) -> Mock:
    """Create a minimal RetrievedChunk-like object for testing."""

    result = Mock()
    result.chunk.content = content

    return result


def test_build_context() -> None:
    results = [
        make_retrieved_chunk("chunk one"),
        make_retrieved_chunk("chunk two"),
    ]

    context = ContextBuilder.build(results)

    assert "[Source 1]" in context
    assert "chunk one" in context
    assert "[Source 2]" in context
    assert "chunk two" in context


def test_empty_context() -> None:
    context = ContextBuilder.build([])

    assert context == ""


def test_rag_prompt_is_grounded() -> None:
    question = "این سند درباره چیست؟"
    context = "این یک سند آزمایشی درباره RAG است."

    prompt = RAGPrompt.build(
        question,
        context,
    )

    assert question in prompt
    assert context in prompt

    assert (
        "فقط از CONTEXT استفاده کن."
        in prompt
    )

    assert "پاسخ این سؤال در اسناد موجود پیدا نشد." in prompt
