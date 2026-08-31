
from app.llm.ollama import OllamaLLMService


def test_remove_thinking_block() -> None:
    text = (
        "<think>\n"
        "internal reasoning\n"
        "</think>\n\n"
        "پاسخ نهایی"
    )

    result = OllamaLLMService._remove_thinking(text)

    assert result == "پاسخ نهایی"


def test_remove_thinking_block_keeps_normal_text() -> None:
    text = "پاسخ نهایی"

    result = OllamaLLMService._remove_thinking(text)

    assert result == "پاسخ نهایی"

