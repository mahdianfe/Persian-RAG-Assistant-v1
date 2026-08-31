from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkService:
    """Service layer for document chunk operations."""

    @staticmethod
    def create_many(
        db: Session,
        document_id: int,
        chunks: list[str],
    ) -> list[DocumentChunk]:
        """Create and persist chunks for a document."""

        document_chunks = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk,
            )
            for index, chunk in enumerate(chunks)
        ]

        if document_chunks:
            db.add_all(document_chunks)
            db.flush()

        return document_chunks

    @staticmethod
    def get_by_document_id(
        db: Session,
        document_id: int,
    ) -> list[DocumentChunk]:
        """Return all chunks belonging to a document."""

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(db.scalars(statement).all())
