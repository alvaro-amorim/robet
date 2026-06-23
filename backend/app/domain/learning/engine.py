from datetime import datetime, timezone

from app.schemas.models import LearningInsight, Recommendation


def generate_learning_insights(recommendations: list[Recommendation]) -> list[LearningInsight]:
    low_odd = [rec for rec in recommendations if rec.odd_decimal < 1.7]
    cards = [rec for rec in recommendations if rec.market == "cards"]
    good = [rec for rec in recommendations if rec.recommendation_type == "GOOD_OPPORTUNITY"]
    return [
        LearningInsight(
            id="insight_mock_001",
            insight_type="odds_baixas",
            description="Odds muito baixas precisam de edge alto para compensar o risco simulado.",
            evidence={"count": len(low_odd), "threshold": 1.7},
            confidence=0.62,
            created_at=datetime.now(timezone.utc),
        ),
        LearningInsight(
            id="insight_mock_002",
            insight_type="mercado_cartoes",
            description="Mercados de cartões estão com confiança menor por falta de dados de árbitro e contexto disciplinar.",
            evidence={"recommendations": len(cards), "confidence_hint": 0.48},
            confidence=0.58,
            created_at=datetime.now(timezone.utc),
        ),
        LearningInsight(
            id="insight_mock_003",
            insight_type="oportunidades",
            description="As melhores recomendações mockadas combinam EV positivo, edge acima do mínimo e confiança moderada.",
            evidence={"good_opportunities": len(good)},
            confidence=0.66,
            created_at=datetime.now(timezone.utc),
        ),
    ]
