
from sqlalchemy.orm import Session

from app.core.config import settings
from app.embedding.service import EmbeddingService
from app.llm.service import LLMService
from app.services.answer_validator import AnswerValidator
from app.services.context import ContextBuilder
from app.services.extractor import ExtractionService
from app.services.prompt import RAGPrompt
from app.services.retrieval import RetrievalService


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
            top_k=20,
            similarity_threshold=(
                settings.retrieval_similarity_threshold
            ),
            document_id=settings.rag_document_id,
        )

        if not chunks:
            return "پاسخ این سؤال در اسناد موجود پیدا نشد."

        best_score = chunks[0].score

        if best_score < settings.rag_min_answer_score:
            return "پاسخ این سؤال در اسناد موجود پیدا نشد."

        context = self.context_builder.build(chunks)

        if not context.strip():
            return "پاسخ این سؤال در اسناد موجود پیدا نشد."

        prompt = RAGPrompt.build(
            question,
            context,
        )

        extracted = ExtractionService.extract_terms(
            question,
            context,
        )

        if extracted:
            return extracted

        answer = self.llm_service.generate(prompt)
  

        validated_answer = AnswerValidator.validate(
            answer,
            context,
        )

        return validated_answer
