from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.services.context import ContextBuilder
from app.services.rag import RAGService
from app.services.retrieval import RetrievalService
from app.db.session import SessionLocal


def build_rag():
    return RAGService(
        embedding_service=OllamaEmbeddingService(),
        retrieval_service=RetrievalService(),
        context_builder=ContextBuilder(),
        llm_service=OllamaLLMService(),
    )


def test_rag_rejects_unrelated_question():

    db = SessionLocal()

    try:
        rag = build_rag()

        answer = rag.answer(
            db,
            "چگونه کیک شکلاتی درست کنیم؟",
        )

        assert (
            answer
            == "پاسخ این سؤال در اسناد موجود پیدا نشد."
        )

    finally:
        db.close()
