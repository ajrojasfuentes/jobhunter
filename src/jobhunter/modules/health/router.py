from fastapi import APIRouter

from jobhunter.modules.health.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Check application liveness")
async def get_health() -> HealthResponse:
    """Confirm that the API responds without checking external dependencies."""
    return HealthResponse(status="ok")
