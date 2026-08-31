import argparse
from pathlib import Path

from sqlalchemy import delete, select

from app.db.session import SessionLocal, transaction
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunking import TextChunkingService
from app.services.document_chunk import DocumentChunkService
from app.services.pdf import PDFService
from app.services.text import TextCleaningService


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Re-ingest an existing PDF into an existing document.",
    )

    parser.add_argument(
        "--document-id",
        type=int,
        required=True,
        help="Existing document ID.",
    )

    parser.add_argument(
        "--pdf",
        type=Path,
        required=True,
        help="Path to the source PDF.",
    )

    return parser.parse_args()


def main() -> None:
    """Re-ingest PDF content and rebuild document chunks."""

    args = parse_args()

    if not args.pdf.is_file():
        raise FileNotFoundError(
            f"PDF file not found: {args.pdf}"
        )

    db = SessionLocal()

    try:
        document = db.scalar(
            select(Document).where(
                Document.id == args.document_id,
            )
        )

        if document is None:
            raise ValueError(
                f"Document {args.document_id} not found."
            )

        extracted_text = PDFService.extract_text(
            args.pdf,
        )

        cleaned_text = TextCleaningService.clean(
            extracted_text,
        )

        if not cleaned_text:
            raise ValueError(
                "No usable text was extracted from the PDF."
            )

        chunking_service = TextChunkingService(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = chunking_service.split(
            cleaned_text,
        )

        if not chunks:
            raise ValueError(
                "No chunks were generated from the PDF."
            )

        with transaction(db):
            document.content = cleaned_text

            db.execute(
                delete(DocumentChunk).where(
                    DocumentChunk.document_id
                    == args.document_id,
                )
            )

            DocumentChunkService.create_many(
                db,
                args.document_id,
                chunks,
            )

        print(
            f"Document {args.document_id} re-ingested successfully."
        )
        print(f"PDF: {args.pdf}")
        print(f"New chunks: {len(chunks)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
