import argparse

from sqlalchemy import delete, select

from app.db.session import SessionLocal, transaction
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.chunking import TextChunkingService
from app.services.document_chunk import DocumentChunkService
from app.services.text import TextCleaningService


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Rebuild chunks for an existing document."
    )

    parser.add_argument(
        "--document-id",
        type=int,
        required=True,
        help="ID of the document to rechunk.",
    )

    return parser.parse_args()


def main() -> None:
    """Rebuild chunks for one document."""

    args = parse_args()
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

        if not document.content:
            raise ValueError(
                f"Document {args.document_id} has no content."
            )

        cleaned_text = TextCleaningService.clean(
            document.content,
        )

        chunking_service = TextChunkingService(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = chunking_service.split(cleaned_text)

        if not chunks:
            raise ValueError(
                f"Document {args.document_id} produced no chunks."
            )

        with transaction(db):
            db.execute(
                delete(DocumentChunk).where(
                    DocumentChunk.document_id == args.document_id,
                )
            )

            DocumentChunkService.create_many(
                db,
                document.id,
                chunks,
            )

        print(
            f"Document {args.document_id} rechunked successfully."
        )
        print(f"New chunks: {len(chunks)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
