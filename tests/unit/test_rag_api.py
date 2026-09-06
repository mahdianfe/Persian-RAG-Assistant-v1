from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_rag_query_endpoint():
    response = client.post(
        "/rag/query",
        json={
            "question": "چه الگوریتم‌هایی در متن نام برده شده‌اند؟"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "Regression" in data["answer"]
