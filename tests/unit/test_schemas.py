from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)


def test_document_create_schema() -> None:
    document = DocumentCreate(
        title="آموزش RAG",
        filename="rag.pdf",
    )

    assert document.title == "آموزش RAG"
    assert document.filename == "rag.pdf"


def test_document_update_schema_partial_update() -> None:
    document = DocumentUpdate(
        title="آموزش پیشرفته RAG",
    )

    data = document.model_dump(
        exclude_unset=True,
    )

    assert data == {
        "title": "آموزش پیشرفته RAG",
    }


def test_document_response_schema() -> None:
    document = DocumentResponse(
        id=1,
        title="آموزش RAG",
        filename="rag.pdf",
        created_at="2026-08-11T10:00:00",
    )

    assert document.id == 1
    assert document.title == "آموزش RAG"
    assert document.filename == "rag.pdf"
