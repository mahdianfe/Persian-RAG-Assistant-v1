from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.documents import router as documents_router
from app.api.routes.rag import router as rag_router
from app.core.exceptions import DatabaseException

app = FastAPI(
    title="Persian RAG Assistant",
    version="0.1.0",
)


@app.exception_handler(DatabaseException)
async def database_exception_handler(
    request: Request,
    exc: DatabaseException,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred.",
        },
    )


app.include_router(documents_router)
app.include_router(rag_router)
