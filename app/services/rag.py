
from sqlalchemy.orm import Session

from app.core.config import settings
from app.embedding.service import EmbeddingService
from app.llm.service import LLMService
from app.services.context import ContextBuilder
from app.services.prompt import RAGPrompt
from app.services.retrieval import RetrievalService


DOCUMENT_ID = 7


class RAGService:
    """Orchestrate retrieval-augmented generation."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        llm_service: LLMService,
    ) -> None:
        self.embedding_service = embedding_service
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.llm_service = llm_service

    def answer(
        self,
        db: Session,
        question: str,
    ) -> str:
        """Generate a grounded answer using retrieved context."""

        query_embedding = self.embedding_service.embed(
            question,
        )

        chunks = self.retrieval_service.search(
            db,
            query_embedding,
            top_k=5,
            similarity_threshold=(
                settings.retrieval_similarity_threshold
            ),
            document_id=DOCUMENT_ID,
        )

        if not chunks:
            return "پاسخ این سؤال در اسناد موجود پیدا نشد."

        context = self.context_builder.build(chunks)

        if not context.strip():
            return "پاسخ این سؤال در اسناد موجود پیدا نشد."

        prompt = RAGPrompt.build(
            question,
            context,
        )

        return self.llm_service.generate(prompt)

