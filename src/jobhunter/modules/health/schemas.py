from typing import Literal

from sqlmodel import SQLModel


class HealthResponse(SQLModel):
    """Public liveness schema; this model is not a database table."""

    status: Literal["ok"]
