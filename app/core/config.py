from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Persian RAG Assistant"
    app_version: str = "0.1.0"
    app_env: str = "development"

    database_url: str

    upload_dir: str = "storage/uploads"
    max_upload_size_mb: int = 20

    ollama_base_url: str
    embedding_model: str = "bge-m3"

    llm_model: str

    retrieval_similarity_threshold: float = 0.42

    rag_min_answer_score: float = 0.40

    rag_document_id: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
