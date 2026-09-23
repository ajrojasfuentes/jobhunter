from importlib.metadata import version

from fastapi import FastAPI
from fastapi.testclient import TestClient

from jobhunter.core.config import Settings
from jobhunter.main import create_app


def test_application_uses_explicit_settings() -> None:
    application = create_app(Settings(_env_file=None, app_name="Test API"))
    assert application.title == "Test API"


def test_application_instances_are_isolated(app: FastAPI) -> None:
    app.state.test_value = "local"
    other = create_app(Settings(_env_file=None, app_name="Other API"))
    assert not hasattr(other.state, "test_value")
    assert other.title == "Other API"


def test_openapi_publishes_package_version_and_health_contract(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"] == {"title": "jobhunter", "version": version("jobhunter")}
    operation = schema["paths"]["/health"]["get"]
    assert operation["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/HealthResponse"
    }
    health_schema = schema["components"]["schemas"]["HealthResponse"]
    assert health_schema["required"] == ["status"]
    assert health_schema["properties"]["status"]["const"] == "ok"
