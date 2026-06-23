from fastapi import APIRouter

from app.core.config import get_settings
from app.core.security_flags import get_security_flags

router = APIRouter()


@router.get("/settings")
def settings() -> dict:
    app_settings = get_settings()
    return {
        "use_mock_providers": app_settings.use_mock_providers,
        "combined_bet_correlation_mode": app_settings.combined_bet_correlation_mode,
        "combined_bet_default_correlation_penalty": app_settings.combined_bet_default_correlation_penalty,
        "security_flags": get_security_flags(app_settings),
    }
