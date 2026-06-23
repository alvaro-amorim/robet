"""initial persisted mvp schema

Revision ID: 20260623_0001
Revises: 
Create Date: 2026-06-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "matches",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("competition", sa.String(), nullable=False),
        sa.Column("home_team", sa.String(), nullable=False),
        sa.Column("away_team", sa.String(), nullable=False),
        sa.Column("commence_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bankroll_snapshots",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("initial_balance", sa.Float(), nullable=False),
        sa.Column("current_balance", sa.Float(), nullable=False),
        sa.Column("simulated_exposure", sa.Float(), nullable=False),
        sa.Column("simulated_profit_loss", sa.Float(), nullable=False),
        sa.Column("total_recommendations", sa.Integer(), nullable=False),
        sa.Column("won", sa.Integer(), nullable=False),
        sa.Column("lost", sa.Integer(), nullable=False),
        sa.Column("pending", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bankroll_snapshots_created_at"), "bankroll_snapshots", ["created_at"], unique=False)
    op.create_table(
        "learning_insights",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("insight_type", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "odds_snapshots",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("match_id", sa.String(), nullable=False),
        sa.Column("bookmaker", sa.String(), nullable=False),
        sa.Column("market", sa.String(), nullable=False),
        sa.Column("selection", sa.String(), nullable=False),
        sa.Column("odd_decimal", sa.Float(), nullable=False),
        sa.Column("point", sa.Float(), nullable=True),
        sa.Column("point_key", sa.String(), nullable=False),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("match_id", "bookmaker", "market", "selection", "point_key", name="uq_odds_snapshot_seed"),
    )
    op.create_index(op.f("ix_odds_snapshots_match_id"), "odds_snapshots", ["match_id"], unique=False)
    op.create_table(
        "recommendations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("match_id", sa.String(), nullable=False),
        sa.Column("market", sa.String(), nullable=False),
        sa.Column("selection", sa.String(), nullable=False),
        sa.Column("odd_decimal", sa.Float(), nullable=False),
        sa.Column("implied_probability", sa.Float(), nullable=False),
        sa.Column("model_probability", sa.Float(), nullable=False),
        sa.Column("edge", sa.Float(), nullable=False),
        sa.Column("expected_value", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("quality_score", sa.Integer(), nullable=False),
        sa.Column("risk_label", sa.String(), nullable=False),
        sa.Column("recommendation_type", sa.String(), nullable=False),
        sa.Column("explanation", sa.String(), nullable=False),
        sa.Column("simulated_stake", sa.Float(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_recommendations_match_id"), "recommendations", ["match_id"], unique=False)
    op.create_table(
        "combined_bets",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("match_id", sa.String(), nullable=False),
        sa.Column("offered_combined_odd", sa.Float(), nullable=False),
        sa.Column("fair_combined_odd_estimate", sa.Float(), nullable=False),
        sa.Column("estimated_joint_probability", sa.Float(), nullable=False),
        sa.Column("adjusted_joint_probability", sa.Float(), nullable=False),
        sa.Column("implied_probability", sa.Float(), nullable=False),
        sa.Column("edge", sa.Float(), nullable=False),
        sa.Column("expected_value", sa.Float(), nullable=False),
        sa.Column("correlation_penalty", sa.Float(), nullable=False),
        sa.Column("quality_score", sa.Integer(), nullable=False),
        sa.Column("risk_label", sa.String(), nullable=False),
        sa.Column("recommendation", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_combined_bets_match_id"), "combined_bets", ["match_id"], unique=False)
    op.create_table(
        "combined_bet_legs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("combined_bet_id", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("market", sa.String(), nullable=False),
        sa.Column("selection", sa.String(), nullable=False),
        sa.Column("individual_odd", sa.Float(), nullable=False),
        sa.Column("estimated_probability", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["combined_bet_id"], ["combined_bets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_combined_bet_legs_combined_bet_id"), "combined_bet_legs", ["combined_bet_id"], unique=False)
    op.create_table(
        "rearrangement_suggestions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("combined_bet_id", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("reason", sa.String(), nullable=False),
        sa.Column("new_estimated_quality_score", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["combined_bet_id"], ["combined_bets.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rearrangement_suggestions_combined_bet_id"), "rearrangement_suggestions", ["combined_bet_id"], unique=False)
    op.create_table(
        "simulation_results",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("recommendation_id", sa.String(), nullable=True),
        sa.Column("combined_bet_id", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("stake", sa.Float(), nullable=False),
        sa.Column("profit_loss", sa.Float(), nullable=False),
        sa.Column("result_label", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["combined_bet_id"], ["combined_bets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["recommendation_id"], ["recommendations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_simulation_results_combined_bet_id"), "simulation_results", ["combined_bet_id"], unique=False)
    op.create_index(op.f("ix_simulation_results_recommendation_id"), "simulation_results", ["recommendation_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_simulation_results_recommendation_id"), table_name="simulation_results")
    op.drop_index(op.f("ix_simulation_results_combined_bet_id"), table_name="simulation_results")
    op.drop_table("simulation_results")
    op.drop_index(op.f("ix_rearrangement_suggestions_combined_bet_id"), table_name="rearrangement_suggestions")
    op.drop_table("rearrangement_suggestions")
    op.drop_index(op.f("ix_combined_bet_legs_combined_bet_id"), table_name="combined_bet_legs")
    op.drop_table("combined_bet_legs")
    op.drop_index(op.f("ix_combined_bets_match_id"), table_name="combined_bets")
    op.drop_table("combined_bets")
    op.drop_index(op.f("ix_recommendations_match_id"), table_name="recommendations")
    op.drop_table("recommendations")
    op.drop_index(op.f("ix_odds_snapshots_match_id"), table_name="odds_snapshots")
    op.drop_table("odds_snapshots")
    op.drop_table("learning_insights")
    op.drop_index(op.f("ix_bankroll_snapshots_created_at"), table_name="bankroll_snapshots")
    op.drop_table("bankroll_snapshots")
    op.drop_table("matches")
