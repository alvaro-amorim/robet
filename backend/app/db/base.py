from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    competition: Mapped[str] = mapped_column(String, nullable=False)
    home_team: Mapped[str] = mapped_column(String, nullable=False)
    away_team: Mapped[str] = mapped_column(String, nullable=False)
    commence_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OddsSnapshotModel(Base):
    __tablename__ = "odds_snapshots"
    __table_args__ = (
        UniqueConstraint("match_id", "bookmaker", "market", "selection", "point_key", name="uq_odds_snapshot_seed"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    bookmaker: Mapped[str] = mapped_column(String, nullable=False)
    market: Mapped[str] = mapped_column(String, nullable=False)
    selection: Mapped[str] = mapped_column(String, nullable=False)
    odd_decimal: Mapped[float] = mapped_column(Float, nullable=False)
    point: Mapped[float | None] = mapped_column(Float, nullable=True)
    point_key: Mapped[str] = mapped_column(String, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class RecommendationModel(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    market: Mapped[str] = mapped_column(String, nullable=False)
    selection: Mapped[str] = mapped_column(String, nullable=False)
    odd_decimal: Mapped[float] = mapped_column(Float, nullable=False)
    implied_probability: Mapped[float] = mapped_column(Float, nullable=False)
    model_probability: Mapped[float] = mapped_column(Float, nullable=False)
    edge: Mapped[float] = mapped_column(Float, nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_label: Mapped[str] = mapped_column(String, nullable=False)
    recommendation_type: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str] = mapped_column(String, nullable=False)
    simulated_stake: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CombinedBetModel(Base):
    __tablename__ = "combined_bets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    offered_combined_odd: Mapped[float] = mapped_column(Float, nullable=False)
    fair_combined_odd_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_joint_probability: Mapped[float] = mapped_column(Float, nullable=False)
    adjusted_joint_probability: Mapped[float] = mapped_column(Float, nullable=False)
    implied_probability: Mapped[float] = mapped_column(Float, nullable=False)
    edge: Mapped[float] = mapped_column(Float, nullable=False)
    expected_value: Mapped[float] = mapped_column(Float, nullable=False)
    correlation_penalty: Mapped[float] = mapped_column(Float, nullable=False)
    quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_label: Mapped[str] = mapped_column(String, nullable=False)
    recommendation: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class CombinedBetLegModel(Base):
    __tablename__ = "combined_bet_legs"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    combined_bet_id: Mapped[str] = mapped_column(ForeignKey("combined_bets.id", ondelete="CASCADE"), nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    market: Mapped[str] = mapped_column(String, nullable=False)
    selection: Mapped[str] = mapped_column(String, nullable=False)
    individual_odd: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_probability: Mapped[float] = mapped_column(Float, nullable=False)


class RearrangementSuggestionModel(Base):
    __tablename__ = "rearrangement_suggestions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    combined_bet_id: Mapped[str] = mapped_column(ForeignKey("combined_bets.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    new_estimated_quality_score: Mapped[int] = mapped_column(Integer, nullable=False)


class BankrollSnapshotModel(Base):
    __tablename__ = "bankroll_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    initial_balance: Mapped[float] = mapped_column(Float, nullable=False)
    current_balance: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_exposure: Mapped[float] = mapped_column(Float, nullable=False)
    simulated_profit_loss: Mapped[float] = mapped_column(Float, nullable=False)
    total_recommendations: Mapped[int] = mapped_column(Integer, nullable=False)
    won: Mapped[int] = mapped_column(Integer, nullable=False)
    lost: Mapped[int] = mapped_column(Integer, nullable=False)
    pending: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)


class LearningInsightModel(Base):
    __tablename__ = "learning_insights"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    insight_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SimulationResultModel(Base):
    __tablename__ = "simulation_results"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    recommendation_id: Mapped[str | None] = mapped_column(ForeignKey("recommendations.id", ondelete="CASCADE"), nullable=True, index=True)
    combined_bet_id: Mapped[str | None] = mapped_column(ForeignKey("combined_bets.id", ondelete="CASCADE"), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    stake: Mapped[float] = mapped_column(Float, nullable=False)
    profit_loss: Mapped[float] = mapped_column(Float, nullable=False)
    result_label: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
