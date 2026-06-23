from fastapi import APIRouter

from app.core.config import get_settings
from app.core.security_flags import get_security_flags

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "mode": "mock" if settings.use_mock_providers else "real_api",
        "security_flags": get_security_flags(settings),
    }
