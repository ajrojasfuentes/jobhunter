from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_body(client: TestClient) -> None:
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_content_type(client: TestClient) -> None:
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"
