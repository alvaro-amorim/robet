from enum import StrEnum

from app.core.config import Settings


class ForbiddenCapability(StrEnum):
    REAL_MONEY = "real_money"
    AUTO_BETTING = "auto_betting"
    BOOKMAKER_SCRAPING = "bookmaker_scraping"
    ANTIBOT_BYPASS = "antibot_bypass"
    LOGGED_BOOKMAKER_AUTOMATION = "logged_bookmaker_automation"
    LIVE_MODE = "live_mode"


class SecurityFlagError(RuntimeError):
    pass


def assert_capability_allowed(capability: ForbiddenCapability, settings: Settings) -> None:
    blocked = {
        ForbiddenCapability.REAL_MONEY: not settings.enable_real_money_mode,
        ForbiddenCapability.AUTO_BETTING: not settings.enable_auto_betting,
        ForbiddenCapability.BOOKMAKER_SCRAPING: not settings.enable_bookmaker_scraping,
        ForbiddenCapability.ANTIBOT_BYPASS: not settings.enable_antibot_bypass,
        ForbiddenCapability.LOGGED_BOOKMAKER_AUTOMATION: not settings.enable_logged_bookmaker_automation,
        ForbiddenCapability.LIVE_MODE: not settings.enable_live_mode,
    }
    if blocked[capability]:
        raise SecurityFlagError(f"Funcionalidade bloqueada por flag de segurança: {capability.value}")


def get_security_flags(settings: Settings) -> dict[str, bool]:
    return {
        "ENABLE_REAL_MONEY_MODE": settings.enable_real_money_mode,
        "ENABLE_AUTO_BETTING": settings.enable_auto_betting,
        "ENABLE_BOOKMAKER_SCRAPING": settings.enable_bookmaker_scraping,
        "ENABLE_ANTIBOT_BYPASS": settings.enable_antibot_bypass,
        "ENABLE_LOGGED_BOOKMAKER_AUTOMATION": settings.enable_logged_bookmaker_automation,
        "ENABLE_LIVE_MODE": settings.enable_live_mode,
    }
