from app.db.session import SessionLocal
from app.embedding.ollama import OllamaEmbeddingService
from app.services.retrieval import RetrievalService


DOCUMENT_ID = 7


def search_question(
    db,
    embedding_service: OllamaEmbeddingService,
    retrieval_service: RetrievalService,
    question: str,
) -> None:
    """Run retrieval for one question and print the results."""

    query_embedding = embedding_service.embed(question)

    results = retrieval_service.search(
        db,
        query_embedding,
        top_k=5,
        similarity_threshold=None,
        document_id=DOCUMENT_ID,
    )

    print("\n" + "=" * 70)
    print(f"Question: {question}")
    print("=" * 70)

    if not results:
        print("No results.")
        return

    for rank, result in enumerate(results, start=1):
        print(
            f"\nRank: {rank}"
            f"\nChunk ID: {result.chunk.id}"
            f"\nDocument ID: {result.chunk.document_id}"
            f"\nChunk Index: {result.chunk.chunk_index}"
            f"\nDistance: {result.distance:.4f}"
            f"\nSimilarity: {result.score:.4f}"
        )
        print(f"Content: {result.chunk.content[:500]}")


def main() -> None:
    """Interactively test retrieval for document 7."""

    db = SessionLocal()

    try:
        embedding_service = OllamaEmbeddingService()
        retrieval_service = RetrievalService()

        print("Interactive retrieval test")
        print("Document ID:", DOCUMENT_ID)
        print("Type 'exit' to quit.")

        while True:
            question = input("\nQuestion: ").strip()

            if question.lower() == "exit":
                break

            if not question:
                print("Question cannot be empty.")
                continue

            search_question(
                db,
                embedding_service,
                retrieval_service,
                question,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
