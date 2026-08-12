def test_create_document(client) -> None:
    response = client.post(
        "/documents",
        json={
            "title": "آموزش RAG",
            "filename": "rag.pdf",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "آموزش RAG"
    assert data["filename"] == "rag.pdf"
    assert "created_at" in data


def test_get_documents(client) -> None:
    client.post(
        "/documents",
        json={
            "title": "سند اول",
            "filename": "first.pdf",
        },
    )

    client.post(
        "/documents",
        json={
            "title": "سند دوم",
            "filename": "second.pdf",
        },
    )

    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "سند اول"
    assert data[1]["title"] == "سند دوم"


def test_get_document_by_id(client) -> None:
    create_response = client.post(
        "/documents",
        json={
            "title": "سند تست",
            "filename": "test.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["title"] == "سند تست"


def test_get_nonexistent_document(client) -> None:
    response = client.get("/documents/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Document not found",
    }


def test_update_document(client) -> None:
    create_response = client.post(
        "/documents",
        json={
            "title": "عنوان قدیمی",
            "filename": "old.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = client.patch(
        f"/documents/{document_id}",
        json={
            "title": "عنوان جدید",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["title"] == "عنوان جدید"
    assert data["filename"] == "old.pdf"


def test_delete_document(client) -> None:
    create_response = client.post(
        "/documents",
        json={
            "title": "سند برای حذف",
            "filename": "delete.pdf",
        },
    )

    document_id = create_response.json()["id"]

    response = client.delete(
        f"/documents/{document_id}",
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/documents/{document_id}",
    )

    assert get_response.status_code == 404
