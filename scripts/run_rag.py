from app.db.session import SessionLocal
from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.services.context import ContextBuilder
from app.services.rag import RAGService
from app.services.retrieval import RetrievalService


def main() -> None:
    """Interactive RAG test."""

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

        print("Interactive RAG test")
        print("Type 'exit' to quit.")

        while True:
            question = input("\nQuestion: ").strip()

            if question.lower() == "exit":
                break

            if not question:
                print("Question cannot be empty.")
                continue

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
