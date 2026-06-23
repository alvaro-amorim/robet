from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.base import (
    BankrollSnapshotModel,
    CombinedBetLegModel,
    CombinedBetModel,
    LearningInsightModel,
    MatchModel,
    OddsSnapshotModel,
    RearrangementSuggestionModel,
    RecommendationModel,
    SimulationResultModel,
)
from app.schemas.models import (
    Bankroll,
    CombinedBet,
    CombinedBetLeg,
    LearningInsight,
    Match,
    OddsSnapshot,
    RearrangementSuggestion,
    Recommendation,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def point_key(point: float | None) -> str:
    return "none" if point is None else str(point)


def upsert_match(db: Session, match: Match) -> MatchModel:
    model = db.get(MatchModel, match.id)
    if model is None:
        model = MatchModel(id=match.id, created_at=utcnow())
    model.competition = match.competition
    model.home_team = match.home_team
    model.away_team = match.away_team
    model.commence_time = match.commence_time
    model.status = match.status
    db.add(model)
    return model


def list_matches(db: Session) -> list[Match]:
    rows = db.scalars(select(MatchModel).order_by(MatchModel.commence_time)).all()
    return [Match(id=row.id, competition=row.competition, home_team=row.home_team, away_team=row.away_team, commence_time=row.commence_time, status=row.status) for row in rows]


def upsert_odds_snapshot(db: Session, odds: OddsSnapshot, odds_id: str) -> OddsSnapshotModel:
    model = db.get(OddsSnapshotModel, odds_id)
    if model is None:
        model = OddsSnapshotModel(id=odds_id)
    model.match_id = odds.match_id
    model.bookmaker = odds.bookmaker
    model.market = odds.market
    model.selection = odds.selection
    model.odd_decimal = odds.odd_decimal
    model.point = odds.point
    model.point_key = point_key(odds.point)
    model.captured_at = odds.captured_at
    db.add(model)
    return model


def list_odds_snapshots(db: Session) -> list[OddsSnapshot]:
    rows = db.scalars(select(OddsSnapshotModel).order_by(OddsSnapshotModel.match_id, OddsSnapshotModel.market)).all()
    return [
        OddsSnapshot(
            match_id=row.match_id,
            bookmaker=row.bookmaker,
            market=row.market,
            selection=row.selection,
            odd_decimal=row.odd_decimal,
            point=row.point,
            captured_at=row.captured_at,
        )
        for row in rows
    ]


def upsert_recommendation(db: Session, recommendation: Recommendation) -> RecommendationModel:
    model = db.get(RecommendationModel, recommendation.id)
    if model is None:
        model = RecommendationModel(id=recommendation.id, created_at=utcnow())
    model.match_id = recommendation.match_id
    model.market = recommendation.market
    model.selection = recommendation.selection
    model.odd_decimal = recommendation.odd_decimal
    model.implied_probability = recommendation.implied_probability
    model.model_probability = recommendation.model_probability
    model.edge = recommendation.edge
    model.expected_value = recommendation.expected_value
    model.confidence = recommendation.confidence
    model.quality_score = recommendation.quality_score
    model.risk_label = recommendation.risk_label
    model.recommendation_type = recommendation.recommendation_type
    model.explanation = recommendation.explanation
    model.simulated_stake = recommendation.simulated_stake
    model.status = recommendation.status
    db.add(model)
    return model


def list_recommendations(db: Session) -> list[Recommendation]:
    rows = db.scalars(select(RecommendationModel).order_by(RecommendationModel.quality_score.desc(), RecommendationModel.id)).all()
    return [
        Recommendation(
            id=row.id,
            match_id=row.match_id,
            market=row.market,
            selection=row.selection,
            odd_decimal=row.odd_decimal,
            implied_probability=row.implied_probability,
            model_probability=row.model_probability,
            edge=row.edge,
            expected_value=row.expected_value,
            confidence=row.confidence,
            quality_score=row.quality_score,
            risk_label=row.risk_label,
            recommendation_type=row.recommendation_type,
            explanation=row.explanation,
            simulated_stake=row.simulated_stake,
            status=row.status,
        )
        for row in rows
    ]


def save_combined_bet(db: Session, combined_bet: CombinedBet) -> CombinedBetModel:
    model = CombinedBetModel(
        id=combined_bet.id,
        match_id=combined_bet.match_id,
        offered_combined_odd=combined_bet.offered_combined_odd,
        fair_combined_odd_estimate=combined_bet.fair_combined_odd_estimate,
        estimated_joint_probability=combined_bet.estimated_joint_probability,
        adjusted_joint_probability=combined_bet.adjusted_joint_probability,
        implied_probability=combined_bet.implied_probability,
        edge=combined_bet.edge,
        expected_value=combined_bet.expected_value,
        correlation_penalty=combined_bet.correlation_penalty,
        quality_score=combined_bet.quality_score,
        risk_label=combined_bet.risk_label,
        recommendation=combined_bet.recommendation,
        created_at=utcnow(),
    )
    db.add(model)
    db.flush()
    for position, leg in enumerate(combined_bet.legs, start=1):
        db.add(
            CombinedBetLegModel(
                id=f"{combined_bet.id}_leg_{position}",
                combined_bet_id=combined_bet.id,
                position=position,
                market=leg.market,
                selection=leg.selection,
                individual_odd=leg.individual_odd,
                estimated_probability=leg.estimated_probability,
            )
        )
    for position, suggestion in enumerate(combined_bet.rearrangement_suggestions, start=1):
        db.add(
            RearrangementSuggestionModel(
                id=f"{combined_bet.id}_suggestion_{position}",
                combined_bet_id=combined_bet.id,
                type=suggestion.type,
                reason=suggestion.reason,
                new_estimated_quality_score=suggestion.new_estimated_quality_score,
            )
        )
    return model


def list_combined_bets(db: Session) -> list[CombinedBet]:
    rows = db.scalars(select(CombinedBetModel).order_by(CombinedBetModel.created_at.desc())).all()
    results: list[CombinedBet] = []
    for row in rows:
        leg_rows = db.scalars(select(CombinedBetLegModel).where(CombinedBetLegModel.combined_bet_id == row.id).order_by(CombinedBetLegModel.position)).all()
        suggestion_rows = db.scalars(select(RearrangementSuggestionModel).where(RearrangementSuggestionModel.combined_bet_id == row.id)).all()
        legs = [CombinedBetLeg(market=leg.market, selection=leg.selection, individual_odd=leg.individual_odd, estimated_probability=leg.estimated_probability) for leg in leg_rows]
        suggestions = [RearrangementSuggestion(type=item.type, reason=item.reason, new_estimated_quality_score=item.new_estimated_quality_score) for item in suggestion_rows]
        results.append(
            CombinedBet(
                id=row.id,
                match_id=row.match_id,
                legs=legs,
                individual_odds=[leg.individual_odd for leg in legs],
                offered_combined_odd=row.offered_combined_odd,
                fair_combined_odd_estimate=row.fair_combined_odd_estimate,
                estimated_joint_probability=row.estimated_joint_probability,
                adjusted_joint_probability=row.adjusted_joint_probability,
                implied_probability=row.implied_probability,
                edge=row.edge,
                expected_value=row.expected_value,
                correlation_penalty=row.correlation_penalty,
                quality_score=row.quality_score,
                risk_label=row.risk_label,
                recommendation=row.recommendation,
                rearrangement_suggestions=suggestions,
            )
        )
    return results


def save_bankroll_snapshot(db: Session, bankroll: Bankroll, snapshot_id: str | None = None) -> BankrollSnapshotModel:
    model = db.get(BankrollSnapshotModel, snapshot_id) if snapshot_id else None
    if model is None:
        model = BankrollSnapshotModel(id=snapshot_id or f"bankroll_{utcnow().timestamp()}", created_at=utcnow())
    model.initial_balance = bankroll.initial_balance
    model.current_balance = bankroll.current_balance
    model.simulated_exposure = bankroll.simulated_exposure
    model.simulated_profit_loss = bankroll.simulated_profit_loss
    model.total_recommendations = bankroll.total_recommendations
    model.won = bankroll.won
    model.lost = bankroll.lost
    model.pending = bankroll.pending
    db.add(model)
    return model


def get_latest_bankroll(db: Session) -> Bankroll | None:
    row = db.scalars(select(BankrollSnapshotModel).order_by(BankrollSnapshotModel.created_at.desc())).first()
    if row is None:
        return None
    return Bankroll(
        initial_balance=row.initial_balance,
        current_balance=row.current_balance,
        simulated_exposure=row.simulated_exposure,
        simulated_profit_loss=row.simulated_profit_loss,
        total_recommendations=row.total_recommendations,
        won=row.won,
        lost=row.lost,
        pending=row.pending,
    )


def upsert_learning_insight(db: Session, insight: LearningInsight) -> LearningInsightModel:
    model = db.get(LearningInsightModel, insight.id)
    if model is None:
        model = LearningInsightModel(id=insight.id)
    model.insight_type = insight.insight_type
    model.description = insight.description
    model.evidence = dict(insight.evidence)
    model.confidence = insight.confidence
    model.created_at = insight.created_at
    db.add(model)
    return model


def list_learning_insights(db: Session) -> list[LearningInsight]:
    rows = db.scalars(select(LearningInsightModel).order_by(LearningInsightModel.created_at.desc(), LearningInsightModel.id)).all()
    return [
        LearningInsight(id=row.id, insight_type=row.insight_type, description=row.description, evidence=row.evidence, confidence=row.confidence, created_at=row.created_at)
        for row in rows
    ]


def upsert_simulation_result(
    db: Session,
    result_id: str,
    status: str,
    stake: float,
    profit_loss: float,
    result_label: str,
    recommendation_id: str | None = None,
    combined_bet_id: str | None = None,
) -> SimulationResultModel:
    model = db.get(SimulationResultModel, result_id)
    if model is None:
        model = SimulationResultModel(id=result_id, created_at=utcnow())
    model.recommendation_id = recommendation_id
    model.combined_bet_id = combined_bet_id
    model.status = status
    model.stake = stake
    model.profit_loss = profit_loss
    model.result_label = result_label
    db.add(model)
    return model


def clear_development_data(db: Session) -> None:
    for model in [
        SimulationResultModel,
        RearrangementSuggestionModel,
        CombinedBetLegModel,
        CombinedBetModel,
        LearningInsightModel,
        BankrollSnapshotModel,
        RecommendationModel,
        OddsSnapshotModel,
        MatchModel,
    ]:
        db.execute(delete(model))
