from pathlib import Path

from sqlalchemy.orm import Session

from app.schemas.document import DocumentCreate
from app.services.chunking import TextChunkingService
from app.services.document import DocumentService
from app.services.document_chunk import DocumentChunkService
from app.services.embedding import DocumentChunkEmbeddingService
from app.services.pdf import PDFService
from app.services.text import TextCleaningService


class DocumentIngestionService:
    """Complete pipeline for PDF ingestion."""

    def __init__(
        self,
        chunking_service: TextChunkingService | None = None,
        embedding_service: DocumentChunkEmbeddingService | None = None,
    ) -> None:

        self.chunking_service = (
            chunking_service
            or TextChunkingService(
                chunk_size=1000,
                chunk_overlap=200,
            )
        )

        self.embedding_service = (
            embedding_service
            or DocumentChunkEmbeddingService()
        )

    def ingest(
        self,
        db: Session,
        file_path: Path,
        filename: str,
    ):

        extracted_text = PDFService.extract_text(
            file_path,
        )

        cleaned_text = TextCleaningService.clean(
            extracted_text,
        )

        if not cleaned_text:
            raise ValueError(
                "No usable text found in PDF."
            )

        document = DocumentService.create(
            db,
            DocumentCreate(
                title=Path(filename).stem,
                filename=filename,
            ),
            content=cleaned_text,
        )

        chunks = self.chunking_service.split(
            cleaned_text,
        )

        DocumentChunkService.create_many(
            db,
            document.id,
            chunks,
        )

        self.embedding_service.embed_pending_chunks(
            db,
        )

        return document
