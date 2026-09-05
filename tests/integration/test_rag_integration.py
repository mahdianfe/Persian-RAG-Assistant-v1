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


def create_rag_service():
    return RAGService(
        embedding_service=OllamaEmbeddingService(),
        retrieval_service=RetrievalService(),
        context_builder=ContextBuilder(),
        llm_service=OllamaLLMService(),
    )


def test_rag_answers():
    db = SessionLocal()

    try:
        rag_service = create_rag_service()

        for case in TEST_CASES:
            answer = rag_service.answer(
                db,
                case["question"],
            )

            if case["expected"] == "not_found":
                assert (
                    "پاسخ این سؤال در اسناد موجود پیدا نشد."
                    in answer
                )

            else:
                for keyword in case["keywords"]:
                    assert keyword in answer

    finally:
        db.close()
