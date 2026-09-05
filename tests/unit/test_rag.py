from unittest.mock import Mock

from app.services.rag import RAGService
from app.services.retrieval import RetrievedChunk


def test_rag_service_returns_generated_answer() -> None:
    db = Mock()

    embedding_service = Mock()
    retrieval_service = Mock()
    context_builder = Mock()
    llm_service = Mock()

    embedding_service.embed.return_value = [0.1, 0.2]

    fake_chunk = Mock()

    retrieval_service.search.return_value = [
        RetrievedChunk(
            chunk=fake_chunk,
            distance=0.2,
            score=0.8,
        )
    ]

    context_builder.build.return_value = "Relevant context"

    context_builder.build.return_value = (
        "این یک context معتبر برای آزمایش سیستم RAG است که طول کافی دارد."
)

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
