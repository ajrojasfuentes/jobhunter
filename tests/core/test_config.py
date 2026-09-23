from pathlib import Path

import pytest
from pydantic import ValidationError

from jobhunter.core.config import Settings
from jobhunter.main import create_app


@pytest.fixture(autouse=True)
def isolated_settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("JOBHUNTER_APP_NAME", raising=False)
    monkeypatch.delenv("jobhunter_app_name", raising=False)


def test_settings_defaults() -> None:
    assert Settings().app_name == "jobhunter"


def test_application_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JOBHUNTER_APP_NAME", "Environment API")
    assert create_app().title == "Environment API"


def test_dotenv_is_loaded(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        "JOBHUNTER_APP_NAME=Local API\nUNRELATED_VALUE=ignored\n", encoding="utf-8"
    )
    assert Settings().app_name == "Local API"


def test_environment_overrides_dotenv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("JOBHUNTER_APP_NAME=Local API\n", encoding="utf-8")
    monkeypatch.setenv("JOBHUNTER_APP_NAME", "Environment API")
    assert Settings().app_name == "Environment API"


@pytest.mark.parametrize("app_name", ["", "   "])
def test_empty_application_name_is_rejected(app_name: str) -> None:
    with pytest.raises(ValidationError, match="app_name"):
        Settings(app_name=app_name)
