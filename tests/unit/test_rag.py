from unittest.mock import Mock

from app.core.config import settings
from app.services.rag import RAGService


def test_rag_service_returns_generated_answer() -> None:
    db = Mock()

    embedding_service = Mock()
    retrieval_service = Mock()
    context_builder = Mock()
    llm_service = Mock()

    embedding_service.embed.return_value = [0.1, 0.2]
    retrieval_service.search.return_value = ["chunk1", "chunk2"]
    context_builder.build.return_value = "Relevant context"
    llm_service.generate.return_value = "Final answer"

    service = RAGService(
        embedding_service=embedding_service,
        retrieval_service=retrieval_service,
        context_builder=context_builder,
        llm_service=llm_service,
    )

    result = service.answer(
        db,
        "RAG چیست؟",
    )

    assert result == "Final answer"

    embedding_service.embed.assert_called_once_with(
        "RAG چیست؟",
    )

    retrieval_service.search.assert_called_once_with(
        db,
        embedding_service.embed.return_value,
        top_k=5,
        similarity_threshold=settings.retrieval_similarity_threshold,
        document_id=7,
    )

    context_builder.build.assert_called_once_with(
        retrieval_service.search.return_value,
    )

    llm_service.generate.assert_called_once()

    generated_prompt = llm_service.generate.call_args.args[0]

    assert "Relevant context" in generated_prompt
    assert "RAG چیست؟" in generated_prompt

    assert (
        "به سؤال کاربر فقط و فقط بر اساس اطلاعات صریح موجود در CONTEXT پاسخ بده."
        in generated_prompt
    )

    assert "پاسخ این سؤال در اسناد موجود پیدا نشد." in generated_prompt
