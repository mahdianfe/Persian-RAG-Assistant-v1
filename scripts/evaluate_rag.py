
from app.db.session import SessionLocal
from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.services.context import ContextBuilder
from app.services.prompt import RAGPrompt
from app.services.retrieval import RetrievalService


DOCUMENT_ID = 7
TOP_K = 5
SIMILARITY_THRESHOLD = 0.35

QUESTIONS = [
    "یادگیری ماشین چیست؟",
    "یادگیری ماشین چه تفاوتی با برنامه‌نویسی سنتی دارد؟",
    "انواع اصلی یادگیری ماشین چیست؟",
    "رگرسیون چیست؟",
    "خوشه‌بندی چیست؟",
    "پایتخت فرانسه چیست؟",
]


def evaluate_question(
    question: str,
    embedding_service: OllamaEmbeddingService,
    retrieval_service: RetrievalService,
    context_builder: ContextBuilder,
    llm_service: OllamaLLMService,
    db,
) -> None:
    """Run one question through the complete RAG pipeline."""

    query_embedding = embedding_service.embed(question)

    results = retrieval_service.search(
        db,
        query_embedding,
        top_k=TOP_K,
        similarity_threshold=SIMILARITY_THRESHOLD,
        document_id=DOCUMENT_ID,
    )

    context = context_builder.build(results)

    print("\n" + "=" * 80)
    print(f"QUESTION: {question}")
    print("=" * 80)

    print("\n--- RETRIEVED CHUNKS ---")

    if not results:
        print("No chunks retrieved.")
    else:
        for rank, result in enumerate(results, start=1):
            print(
                f"\nRank: {rank}"
                f"\nChunk Index: {result.chunk.chunk_index}"
                f"\nSimilarity: {result.score:.4f}"
                f"\nContent: {result.chunk.content[:300]}"
            )

    print("\n--- CONTEXT ---")
    if context.strip():
        print(context)
    else:
        print("EMPTY")

    print("\n--- ANSWER ---")

    if not context.strip():
        print("پاسخ این سؤال در اسناد موجود پیدا نشد.")
        return

    prompt = RAGPrompt.build(
        question,
        context,
    )

    answer = llm_service.generate(prompt)

    print(answer)


def main() -> None:
    """Evaluate the RAG pipeline with a fixed set of questions."""

    db = SessionLocal()

    try:
        embedding_service = OllamaEmbeddingService()
        retrieval_service = RetrievalService()
        context_builder = ContextBuilder()
        llm_service = OllamaLLMService()

        for question in QUESTIONS:
            evaluate_question(
                question=question,
                embedding_service=embedding_service,
                retrieval_service=retrieval_service,
                context_builder=context_builder,
                llm_service=llm_service,
                db=db,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
