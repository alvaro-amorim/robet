import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db.base import (
    BankrollSnapshotModel,
    CombinedBetLegModel,
    CombinedBetModel,
    CompetitionModel,
    LearningInsightModel,
    MatchModel,
    OddsSnapshotModel,
    RawApiPayloadModel,
    RearrangementSuggestionModel,
    RecommendationModel,
    SimulationResultModel,
    TeamAliasModel,
    TeamModel,
)
from app.domain.normalization.team import normalize_team_name
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


SENSITIVE_PARAM_KEYS = {"api_key", "apikey", "key", "token", "secret", "x-apisports-key"}


def sanitize_request_params(params: dict | None) -> dict:
    safe_params = {}
    for key, value in (params or {}).items():
        if key.lower() in SENSITIVE_PARAM_KEYS:
            safe_params[key] = "[REDACTED]"
        else:
            safe_params[key] = value
    return safe_params


def calculate_payload_hash(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def save_raw_api_payload(
    db: Session,
    provider: str,
    endpoint: str,
    request_method: str,
    request_params: dict | None,
    response_status: int | None,
    raw_payload: dict,
    source_timestamp: datetime | None = None,
    cost_estimate: float = 1.0,
    error_message: str | None = None,
) -> RawApiPayloadModel:
    payload_hash = calculate_payload_hash(
        {
            "provider": provider,
            "endpoint": endpoint,
            "request_method": request_method.upper(),
            "request_params": sanitize_request_params(request_params),
            "response_status": response_status,
            "raw_payload": raw_payload,
            "error_message": error_message,
        }
    )
    model = RawApiPayloadModel(
        id=f"raw_{uuid4().hex}",
        provider=provider,
        endpoint=endpoint,
        request_method=request_method.upper(),
        request_params_json=sanitize_request_params(request_params),
        response_status=response_status,
        raw_payload_json=raw_payload,
        payload_hash=payload_hash,
        collected_at=utcnow(),
        source_timestamp=source_timestamp,
        cost_estimate=cost_estimate,
        error_message=error_message,
    )
    db.add(model)
    db.flush()
    return model


def count_raw_api_payloads_since(db: Session, provider: str, since: datetime) -> int:
    return int(
        db.scalar(
            select(func.count()).select_from(RawApiPayloadModel).where(
                RawApiPayloadModel.provider == provider,
                RawApiPayloadModel.collected_at >= since,
            )
        )
        or 0
    )


def upsert_competition(
    db: Session,
    external_provider: str,
    external_id: str,
    name: str,
    country: str | None,
    season: int,
    competition_type: str | None,
    is_active: bool,
) -> CompetitionModel:
    existing = db.scalars(
        select(CompetitionModel).where(
            CompetitionModel.external_provider == external_provider,
            CompetitionModel.external_id == str(external_id),
            CompetitionModel.season == season,
        )
    ).first()
    now = utcnow()
    model = existing or CompetitionModel(id=f"{external_provider}_competition_{external_id}_{season}", created_at=now)
    model.external_provider = external_provider
    model.external_id = str(external_id)
    model.name = name
    model.country = country
    model.season = season
    model.type = competition_type
    model.is_active = is_active
    model.updated_at = now
    db.add(model)
    return model


def list_competitions(db: Session, provider: str | None = None, name_contains: str | None = None) -> list[CompetitionModel]:
    statement = select(CompetitionModel).order_by(CompetitionModel.season.desc(), CompetitionModel.name)
    if provider:
        statement = statement.where(CompetitionModel.external_provider == provider)
    if name_contains:
        statement = statement.where(CompetitionModel.name.ilike(f"%{name_contains}%"))
    return list(db.scalars(statement).all())


def upsert_team(db: Session, name: str, country: str | None = None) -> TeamModel:
    normalized_name = normalize_team_name(name)
    model = db.scalars(
        select(TeamModel).where(
            TeamModel.normalized_name == normalized_name,
            TeamModel.country.is_(None) if country is None else TeamModel.country == country,
        )
    ).first()
    now = utcnow()
    if model is None:
        model = TeamModel(id=f"team_{uuid4().hex[:12]}", created_at=now)
    model.name = name
    model.normalized_name = normalized_name
    model.country = country
    model.updated_at = now
    db.add(model)
    return model


def upsert_team_alias(db: Session, team_id: str, provider: str, external_id: str, external_name: str) -> TeamAliasModel:
    model = db.scalars(
        select(TeamAliasModel).where(
            TeamAliasModel.provider == provider,
            TeamAliasModel.external_id == str(external_id),
        )
    ).first()
    now = utcnow()
    if model is None:
        model = TeamAliasModel(id=f"team_alias_{provider}_{external_id}", created_at=now)
    model.team_id = team_id
    model.provider = provider
    model.external_id = str(external_id)
    model.external_name = external_name
    model.updated_at = now
    db.add(model)
    return model


def upsert_real_match(
    db: Session,
    provider: str,
    external_id: str,
    competition: CompetitionModel,
    home_team: TeamModel,
    away_team: TeamModel,
    home_team_name_snapshot: str,
    away_team_name_snapshot: str,
    commence_time: datetime,
    status: str,
    raw_payload_id: str | None,
    home_score: int | None = None,
    away_score: int | None = None,
) -> MatchModel:
    match_id = f"{provider}_fixture_{external_id}"
    now = utcnow()
    model = db.get(MatchModel, match_id)
    if model is None:
        model = MatchModel(id=match_id, created_at=now)
    model.competition_id = competition.id
    model.external_provider = provider
    model.external_id = str(external_id)
    model.home_team_id = home_team.id
    model.away_team_id = away_team.id
    model.competition = competition.name
    model.home_team = home_team.name
    model.away_team = away_team.name
    model.home_team_name_snapshot = home_team_name_snapshot
    model.away_team_name_snapshot = away_team_name_snapshot
    model.commence_time = commence_time
    model.status = status
    model.home_score = home_score
    model.away_score = away_score
    model.raw_payload_id = raw_payload_id
    model.updated_at = now
    db.add(model)
    return model


def upsert_match(db: Session, match: Match) -> MatchModel:
    model = db.get(MatchModel, match.id)
    if model is None:
        model = MatchModel(id=match.id, created_at=utcnow())
    model.competition = match.competition
    model.home_team = match.home_team
    model.away_team = match.away_team
    model.commence_time = match.commence_time
    model.status = match.status
    model.home_team_name_snapshot = match.home_team
    model.away_team_name_snapshot = match.away_team
    model.updated_at = utcnow()
    db.add(model)
    return model


def list_matches(db: Session, only_real: bool = False) -> list[Match]:
    statement = select(MatchModel).order_by(MatchModel.commence_time)
    if only_real:
        statement = statement.where(MatchModel.external_provider.is_not(None))
    rows = db.scalars(statement).all()
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
        TeamAliasModel,
        MatchModel,
        TeamModel,
        CompetitionModel,
        RawApiPayloadModel,
    ]:
        db.execute(delete(model))
