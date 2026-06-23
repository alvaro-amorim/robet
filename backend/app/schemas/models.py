from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field

RecommendationType = Literal["GOOD_OPPORTUNITY", "WATCH", "AVOID", "INSUFFICIENT_DATA", "HIGH_RISK"]
RiskLabel = Literal["baixo", "medio", "alto"]


class Match(BaseModel):
    id: str
    competition: str
    home_team: str
    away_team: str
    commence_time: datetime
    status: str


class OddsSnapshot(BaseModel):
    match_id: str
    bookmaker: str
    market: str
    selection: str
    odd_decimal: float
    point: float | None = None
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Recommendation(BaseModel):
    id: str
    match_id: str
    market: str
    selection: str
    odd_decimal: float
    implied_probability: float
    model_probability: float
    edge: float
    expected_value: float
    confidence: float
    quality_score: int
    risk_label: RiskLabel
    recommendation_type: RecommendationType
    explanation: str
    simulated_stake: float
    status: str = "simulada_pendente"


class CombinedBetLeg(BaseModel):
    market: str
    selection: str
    individual_odd: float = Field(gt=1)
    estimated_probability: float = Field(gt=0, lt=1)


class CombinedBetRequest(BaseModel):
    match_id: str
    offered_combined_odd: float = Field(gt=1)
    legs: list[CombinedBetLeg] = Field(min_length=2)


class RearrangementSuggestion(BaseModel):
    type: str
    reason: str
    new_estimated_quality_score: int


class CombinedBet(BaseModel):
    id: str
    match_id: str
    legs: list[CombinedBetLeg]
    individual_odds: list[float]
    offered_combined_odd: float
    fair_combined_odd_estimate: float
    estimated_joint_probability: float
    adjusted_joint_probability: float
    implied_probability: float
    edge: float
    expected_value: float
    correlation_penalty: float
    quality_score: int
    risk_label: RiskLabel
    recommendation: RecommendationType
    rearrangement_suggestions: list[RearrangementSuggestion]


class Bankroll(BaseModel):
    initial_balance: float
    current_balance: float
    simulated_exposure: float
    simulated_profit_loss: float
    total_recommendations: int
    won: int
    lost: int
    pending: int


class LearningInsight(BaseModel):
    id: str
    insight_type: str
    description: str
    evidence: dict[str, float | int | str]
    confidence: float
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
