from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Robet"
    app_env: str = "development"
    use_mock_providers: bool = True
    database_url: str = "postgresql+psycopg://robet:robet_password@localhost:5432/robet"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    football_data_provider: str = "api_football"
    football_api_base_url: str = "https://v3.football.api-sports.io"
    football_api_key: str = ""
    football_api_timeout_seconds: int = 20
    football_api_cache_ttl_seconds: int = 3600
    football_api_daily_request_limit: int = 100
    football_real_sync_enabled: bool = False
    football_sync_max_requests_per_run: int = 10
    football_world_cup_search_terms: str = "world cup,fifa world cup,copa do mundo"
    football_default_season: int = 2026

    enable_live_mode: bool = False
    enable_real_money_mode: bool = False
    enable_auto_betting: bool = False
    enable_bookmaker_scraping: bool = False
    enable_antibot_bypass: bool = False
    enable_logged_bookmaker_automation: bool = False

    bankroll_initial_balance: float = 1000.0
    max_stake_per_recommendation_percent: float = 1.0
    combined_bet_correlation_mode: str = "conservative_penalty"
    combined_bet_default_correlation_penalty: float = 0.15

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def football_world_cup_search_term_list(self) -> list[str]:
        return [term.strip() for term in self.football_world_cup_search_terms.split(",") if term.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
