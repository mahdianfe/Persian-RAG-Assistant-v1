from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.embedding.ollama import OllamaEmbeddingService
from app.llm.ollama import OllamaLLMService
from app.schemas.rag import (
    RAGQueryRequest,
    RAGQueryResponse,
)
from app.services.context import ContextBuilder
from app.services.rag import RAGService
from app.services.retrieval import RetrievalService


router = APIRouter(
    prefix="/rag",
    tags=["rag"],
)


def create_rag_service() -> RAGService:
    return RAGService(
        embedding_service=OllamaEmbeddingService(),
        retrieval_service=RetrievalService(),
        context_builder=ContextBuilder(),
        llm_service=OllamaLLMService(),
    )


@router.post(
    "/query",
    response_model=RAGQueryResponse,
)
def query_rag(
    data: RAGQueryRequest,
    db: Session = Depends(get_db),
) -> RAGQueryResponse:

    rag_service = create_rag_service()

    answer = rag_service.answer(
        db,
        data.question,
    )

    return RAGQueryResponse(
        answer=answer,
    )
