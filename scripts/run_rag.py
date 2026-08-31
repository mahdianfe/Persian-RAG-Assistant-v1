
from app.db.session import SessionLocal
from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.services.context import ContextBuilder
from app.services.rag import RAGService
from app.services.retrieval import RetrievalService


def main() -> None:
    """Run an end-to-end RAG test."""

    db = SessionLocal()

    try:
        embedding_service = OllamaEmbeddingService()
        retrieval_service = RetrievalService()
        context_builder = ContextBuilder()
        llm_service = OllamaLLMService()

        rag_service = RAGService(
            embedding_service=embedding_service,
            retrieval_service=retrieval_service,
            context_builder=context_builder,
            llm_service=llm_service,
        )

        question = "این سند درباره چه چیزی صحبت می‌کند؟"

        print("\n=== Question ===")
        print(question)

        answer = rag_service.answer(
            db,
            question,
        )

        print("\n=== Answer ===")
        print(answer)

    finally:
        db.close()


if __name__ == "__main__":
    main()
