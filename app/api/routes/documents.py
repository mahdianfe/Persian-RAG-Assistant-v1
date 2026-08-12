from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services.document import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_document_route(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
) -> DocumentResponse:
    return DocumentService.create(db, document_data)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents_route(
    db: Session = Depends(get_db),
) -> list[DocumentResponse]:
    return DocumentService.get_all(db)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document_route(
    document_id: int,
    db: Session = Depends(get_db),
) -> DocumentResponse:
    document = DocumentService.get_by_id(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document


@router.patch(
    "/{document_id}",
    response_model=DocumentResponse,
)
def update_document_route(
    document_id: int,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
) -> DocumentResponse:
    document = DocumentService.get_by_id(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return DocumentService.update(
        db,
        document,
        document_data,
    )


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_document_route(
    document_id: int,
    db: Session = Depends(get_db),
) -> None:
    document = DocumentService.get_by_id(
        db,
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    DocumentService.delete(db, document)
