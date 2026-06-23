from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import bankroll, bet_builder, health, learning, matches, recommendations, settings
from app.core.config import get_settings


def create_app() -> FastAPI:
    app_settings = get_settings()
    app = FastAPI(
        title="Robet API",
        description="Laboratório probabilístico mockado para futebol pré-jogo.",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(matches.router)
    app.include_router(recommendations.router)
    app.include_router(bet_builder.router)
    app.include_router(bankroll.router)
    app.include_router(learning.router)
    app.include_router(settings.router)
    return app


app = create_app()
