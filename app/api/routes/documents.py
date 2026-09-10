from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db, transaction
from app.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentUpdate,
)
from app.services.document import DocumentService
from app.services.ingestion import DocumentIngestionService

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
    with transaction(db):
        return DocumentService.create(
            db,
            document_data,
        )


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    stored_filename = f"{uuid4()}_{file.filename}"
    file_path = upload_dir / stored_filename

    try:
        file_content = await file.read()

        max_size = settings.max_upload_size_mb * 1024 * 1024

        if len(file_content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File is too large.",
            )

        file_path.write_bytes(file_content)


        with transaction(db):
            document = DocumentIngestionService().ingest(
                db,
                file_path,
                file.filename,
            )

        return document

    except HTTPException:
        raise

    except Exception as exc:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process PDF.",
        ) from exc


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

    with transaction(db):
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

    with transaction(db):
        DocumentService.delete(
            db,
            document,
        )
