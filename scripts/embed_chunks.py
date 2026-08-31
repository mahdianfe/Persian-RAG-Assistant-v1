from app.db.session import SessionLocal, transaction
from app.services.embedding import DocumentChunkEmbeddingService


def main() -> None:
    db = SessionLocal()

    try:
        service = DocumentChunkEmbeddingService()

        with transaction(db):
            count = service.embed_pending_chunks(db)

        print(f"Embedded chunks: {count}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
