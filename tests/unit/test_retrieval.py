from unittest.mock import Mock

from app.services.retrieval import RetrievalService


def test_retrieval_returns_similarity_score() -> None:
    db = Mock()

    chunk = Mock()
    chunk.id = 1
    chunk.document_id = 5
    chunk.chunk_index = 0
    chunk.content = "Test content"

    db.execute.return_value.all.return_value = [
        (chunk, 0.2),
    ]

    results = RetrievalService.search(
        db,
        [0.1, 0.2],
        top_k=5,
    )

    assert len(results) == 1
    assert results[0].chunk is chunk
    assert results[0].distance == 0.2
    assert results[0].score == 0.8


def test_retrieval_applies_similarity_threshold() -> None:
    db = Mock()

    chunk = Mock()
    db.execute.return_value.all.return_value = [
        (chunk, 0.4),
    ]

    results = RetrievalService.search(
        db,
        [0.1, 0.2],
        top_k=5,
        similarity_threshold=0.5,
    )

    assert len(results) == 1
    assert results[0].score == 0.6


def test_retrieval_discards_below_threshold() -> None:
    db = Mock()

    chunk = Mock()
    db.execute.return_value.all.return_value = [
        (chunk, 0.8),
    ]

    results = RetrievalService.search(
        db,
        [0.1, 0.2],
        top_k=5,
        similarity_threshold=0.5,
    )

    assert results == []





def test_retrieval_filters_by_document_id() -> None:
    db = Mock()

    chunk = Mock()
    chunk.document_id = 7

    db.execute.return_value.all.return_value = [
        (chunk, 0.2),
    ]

    results = RetrievalService.search(
        db,
        [0.1, 0.2],
        top_k=5,
        document_id=7,
    )

    assert len(results) == 1
    assert results[0].chunk.document_id == 7
