from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentService:
    """Service layer for Document operations."""

    @staticmethod
    def create(
        db: Session,
        document_data: DocumentCreate,
    ) -> Document:
        """Create a new document."""

        document = Document(
            title=document_data.title,
            filename=document_data.filename,
        )

        db.add(document)
        db.flush()
        db.refresh(document)

        return document

    @staticmethod
    def get_all(db: Session) -> list[Document]:
        """Return all documents."""

        statement = select(Document).order_by(Document.id)

        return list(db.scalars(statement).all())

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
    ) -> Document | None:
        """Return a document by its ID."""

        statement = select(Document).where(
            Document.id == document_id,
        )

        return db.scalar(statement)

    @staticmethod
    def update(
        db: Session,
        document: Document,
        document_data: DocumentUpdate,
    ) -> Document:
        """Update an existing document."""

        update_data = document_data.model_dump(
            exclude_unset=True,
        )

        for field, value in update_data.items():
            setattr(document, field, value)

        db.flush()
        db.refresh(document)

        return document

    @staticmethod
    def delete(
        db: Session,
        document: Document,
    ) -> None:
        """Delete an existing document."""

        db.delete(document)
        db.flush()
