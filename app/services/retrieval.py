from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


@dataclass(frozen=True)
class RetrievedChunk:
    """A retrieved chunk with vector similarity metadata."""

    chunk: DocumentChunk
    distance: float
    score: float


class RetrievalService:
    """Service for semantic similarity search."""

    @staticmethod
    def search(
        db: Session,
        query_embedding: list[float],
        top_k: int = 5,
        similarity_threshold: float | None = None,
        document_id: int | None = None,
    ) -> list[RetrievedChunk]:
        """Return the most similar chunks."""

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding,
        )

        statement = (
            select(
                DocumentChunk,
                distance.label("distance"),
            )
            .where(DocumentChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )

        if document_id is not None:
            statement = statement.where(
                DocumentChunk.document_id == document_id,
            )

        rows = db.execute(statement).all()

        results: list[RetrievedChunk] = []

        for chunk, chunk_distance in rows:
            score = 1.0 - float(chunk_distance)

            if (
                similarity_threshold is not None
                and score < similarity_threshold
            ):
                continue

            results.append(
                RetrievedChunk(
                    chunk=chunk,
                    distance=float(chunk_distance),
                    score=score,
                )
            )

        return results
