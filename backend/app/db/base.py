from datetime import datetime

from sqlalchemy import Boolean, JSON, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RawApiPayloadModel(Base):
    __tablename__ = "raw_api_payloads"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    provider: Mapped[str] = mapped_column(String, nullable=False, index=True)
    endpoint: Mapped[str] = mapped_column(String, nullable=False)
    request_method: Mapped[str] = mapped_column(String, nullable=False)
    request_params_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    response_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_payload_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    payload_hash: Mapped[str] = mapped_column(String, nullable=False, index=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cost_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    error_message: Mapped[str | None] = mapped_column(String, nullable=True)


class CompetitionModel(Base):
    __tablename__ = "competitions"
    __table_args__ = (UniqueConstraint("external_provider", "external_id", "season", name="uq_competitions_external_season"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    external_provider: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TeamModel(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("normalized_name", "country", name="uq_teams_normalized_country"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    normalized_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class TeamAliasModel(Base):
    __tablename__ = "team_aliases"
    __table_args__ = (UniqueConstraint("provider", "external_id", name="uq_team_alias_provider_external"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    team_id: Mapped[str] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[str] = mapped_column(String, nullable=False)
    external_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    competition_id: Mapped[str | None] = mapped_column(ForeignKey("competitions.id", ondelete="SET NULL"), nullable=True, index=True)
    external_provider: Mapped[str | None] = mapped_column(String, nullable=True)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    home_team_id: Mapped[str | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True, index=True)
    away_team_id: Mapped[str | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True, index=True)
    competition: Mapped[str] = mapped_column(String, nullable=False)
    home_team: Mapped[str] = mapped_column(String, nullable=False)
    away_team: Mapped[str] = mapped_column(String, nullable=False)
    home_team_name_snapshot: Mapped[str | None] = mapped_column(String, nullable=True)
    away_team_name_snapshot: Mapped[str | None] = mapped_column(String, nullable=True)
    commence_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_payload_id: Mapped[str | None] = mapped_column(ForeignKey("raw_api_payloads.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


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
