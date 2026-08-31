from sqlalchemy import select
from sqlalchemy.orm import Session

from app.embedding.ollama import OllamaEmbeddingService
from app.models.document_chunk import DocumentChunk


class DocumentChunkEmbeddingService:
    """Generate and store embeddings for document chunks."""

    def __init__(
        self,
        embedding_service: OllamaEmbeddingService | None = None,
    ) -> None:
        self.embedding_service = (
            embedding_service or OllamaEmbeddingService()
        )

    def embed_pending_chunks(
        self,
        db: Session,
    ) -> int:
        """Generate embeddings for chunks without embeddings."""

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
            .order_by(DocumentChunk.id)
        )

        chunks = list(db.scalars(statement).all())

        for chunk in chunks:
            chunk.embedding = self.embedding_service.embed(
                chunk.content,
            )

        db.flush()

        return len(chunks)
