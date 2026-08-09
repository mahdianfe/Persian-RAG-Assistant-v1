from fastapi import FastAPI


app = FastAPI(
    title="Persian RAG Assistant",
    description="A Persian document-based RAG assistant.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
