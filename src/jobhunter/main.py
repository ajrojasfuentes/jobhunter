from importlib.metadata import version

from fastapi import FastAPI

from jobhunter.api.router import api_router
from jobhunter.core.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create an application with settings resolved once at startup."""
    if settings is None:
        settings = Settings()

    application = FastAPI(title=settings.app_name, version=version("jobhunter"))
    application.include_router(api_router)
    return application


app = create_app()
