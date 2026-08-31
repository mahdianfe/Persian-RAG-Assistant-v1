import pytest

from app.embedding.service import EmbeddingService


def test_embedding_service_is_abstract() -> None:
    with pytest.raises(TypeError):
        EmbeddingService()
