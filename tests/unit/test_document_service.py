from unittest.mock import Mock

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate
from app.services.document import DocumentService


def test_create_document() -> None:
    db = Mock()

    document_data = DocumentCreate(
        title="Test Document",
        filename="test.pdf",
    )

    result = DocumentService.create(
        db,
        document_data,
    )

    assert isinstance(result, Document)
    assert result.title == "Test Document"
    assert result.filename == "test.pdf"

    db.add.assert_called_once_with(result)
    db.flush.assert_called_once_with()
    db.refresh.assert_called_once_with(result)


def test_update_document() -> None:
    db = Mock()

    document = Document(
        title="Old Title",
        filename="test.pdf",
    )

    document_data = DocumentUpdate(
        title="New Title",
    )

    result = DocumentService.update(
        db,
        document,
        document_data,
    )

    assert result is document
    assert document.title == "New Title"
    assert document.filename == "test.pdf"

    db.flush.assert_called_once_with()
    db.refresh.assert_called_once_with(document)


def test_delete_document() -> None:
    db = Mock()

    document = Document(
        title="Test Document",
        filename="test.pdf",
    )

    DocumentService.delete(
        db,
        document,
    )

    db.delete.assert_called_once_with(document)
    db.flush.assert_called_once_with()
