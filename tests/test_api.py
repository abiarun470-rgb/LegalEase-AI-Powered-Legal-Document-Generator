from fastapi.testclient import TestClient

from backend.main import app


class FakeGenerator:

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date
    ):

        return (
            f"{document_type}\n"
            f"{parties}\n"
            f"{terms}\n"
            f"{effective_date}"
        )


def test_health():

    client = TestClient(app)

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_generate(monkeypatch):

    monkeypatch.setattr(
        "backend.routes.get_generator",
        lambda: FakeGenerator()
    )

    client = TestClient(app)

    response = client.post(

        "/generate",

        json={
            "document_type": "NDA",
            "parties": "A and B",
            "terms": "Confidentiality",
            "effective_date": "October 1, 2026"
        }
    )

    assert response.status_code == 200

    assert (
        "NDA"
        in response.json()["content"]
    )


def test_export_pdf():

    client = TestClient(app)

    response = client.post(

        "/export/pdf",

        json={
            "document_type": "NDA",
            "content": "Draft document"
        }
    )

    assert response.status_code == 200

    assert response.content.startswith(
        b"%PDF"
    )