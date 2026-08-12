from fastapi.testclient import TestClient

from app.core.exceptions import DatabaseException
from app.main import app


def test_database_exception_handler() -> None:
    @app.get("/test-database-error")
    def test_database_error() -> None:
        raise DatabaseException()

    with TestClient(app) as client:
        response = client.get("/test-database-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "A database error occurred.",
    }
