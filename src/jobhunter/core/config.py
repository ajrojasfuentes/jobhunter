from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated startup settings; environment variables override the local .env file."""

    model_config = SettingsConfigDict(
        env_prefix="JOBHUNTER_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
        str_strip_whitespace=True,
    )

    app_name: str = Field(default="jobhunter", min_length=1)
