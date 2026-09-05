from app.db.session import SessionLocal
from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.services.context import ContextBuilder
from app.services.rag import RAGService
from app.services.retrieval import RetrievalService


TEST_CASES = [
    {
        "question": "یادگیری ماشین چیست؟",
        "expected": "answer",
        "keywords": [
            "یادگیری ماشین",
        ],
    },
    {
        "question": "چه واژه‌هایی مانند Python و RAG در متن آمده‌اند؟",
        "expected": "answer",
        "keywords": [
            "Python",
            "RAG",
            "PDF",
            "scikit-learn",
        ],
    },
    {
        "question": "چه الگوریتم‌هایی در متن نام برده شده‌اند؟",
        "expected": "answer",
        "keywords": [
            "Regression",
            "Classification",
            "k-means",
        ],
    },
    {
        "question": "چگونه کیک شکلاتی درست کنیم؟",
        "expected": "not_found",
        "keywords": [],
    },
    {
        "question": "پایتخت فرانسه چیست؟",
        "expected": "not_found",
        "keywords": [],
    },
]


def evaluate_answer(answer: str, case: dict) -> tuple[bool, list[str]]:
    """
    Evaluate one answer.
    """

    if case["expected"] == "not_found":
        ok = (
            "پاسخ این سؤال در اسناد موجود پیدا نشد."
            in answer
        )

        return ok, []


    missing = []

    for keyword in case["keywords"]:
        if keyword not in answer:
            missing.append(keyword)

    return len(missing) == 0, missing



def main() -> None:

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

        passed = 0

        print("\nRAG Evaluation")
        print("=" * 60)


        for case in TEST_CASES:

            question = case["question"]

            answer = rag_service.answer(
                db,
                question,
            )

            ok, missing = evaluate_answer(
                answer,
                case,
            )


            print("\nQuestion:")
            print(question)

            print("\nAnswer:")
            print(answer)


            if ok:
                print("\nResult: PASS")
                passed += 1

            else:
                print("\nResult: FAIL")

                if missing:
                    print(
                        "Missing keywords:",
                        ", ".join(missing)
                    )


            print("-" * 60)


        print(
            f"\nFinal Score: {passed}/{len(TEST_CASES)}"
        )


    finally:
        db.close()



if __name__ == "__main__":
    main()
