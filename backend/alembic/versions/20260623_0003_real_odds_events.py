"""real odds events

Revision ID: 20260623_0003
Revises: 20260623_0002
Create Date: 2026-06-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0003"
down_revision: Union[str, None] = "20260623_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookmakers",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("external_provider", sa.String(), nullable=False),
        sa.Column("external_key", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_provider", "external_key", name="uq_bookmakers_provider_key"),
    )
    op.create_table(
        "markets",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )
    op.create_index(op.f("ix_markets_key"), "markets", ["key"], unique=False)
    op.create_table(
        "odds_events",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("external_provider", sa.String(), nullable=False),
        sa.Column("external_event_id", sa.String(), nullable=False),
        sa.Column("sport_key", sa.String(), nullable=False),
        sa.Column("sport_title", sa.String(), nullable=True),
        sa.Column("commence_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("home_team", sa.String(), nullable=False),
        sa.Column("away_team", sa.String(), nullable=False),
        sa.Column("normalized_home_team", sa.String(), nullable=False),
        sa.Column("normalized_away_team", sa.String(), nullable=False),
        sa.Column("linked_match_id", sa.String(), nullable=True),
        sa.Column("match_link_confidence", sa.Float(), nullable=True),
        sa.Column("raw_payload_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["linked_match_id"], ["matches.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["raw_payload_id"], ["raw_api_payloads.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_provider", "external_event_id", "sport_key", name="uq_odds_events_external"),
    )
    op.create_index(op.f("ix_odds_events_sport_key"), "odds_events", ["sport_key"], unique=False)
    op.create_index(op.f("ix_odds_events_normalized_home_team"), "odds_events", ["normalized_home_team"], unique=False)
    op.create_index(op.f("ix_odds_events_normalized_away_team"), "odds_events", ["normalized_away_team"], unique=False)
    op.create_index(op.f("ix_odds_events_linked_match_id"), "odds_events", ["linked_match_id"], unique=False)

    op.add_column("odds_snapshots", sa.Column("odds_event_id", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("raw_payload_id", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("bookmaker_id", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("market_id", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("market_key", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("selection_name", sa.String(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("implied_probability", sa.Float(), nullable=True))
    op.add_column("odds_snapshots", sa.Column("source_last_update", sa.DateTime(timezone=True), nullable=True))
    op.add_column("odds_snapshots", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.alter_column("odds_snapshots", "match_id", existing_type=sa.String(), nullable=True)
    op.create_index(op.f("ix_odds_snapshots_odds_event_id"), "odds_snapshots", ["odds_event_id"], unique=False)
    op.create_index(op.f("ix_odds_snapshots_bookmaker_id"), "odds_snapshots", ["bookmaker_id"], unique=False)
    op.create_index(op.f("ix_odds_snapshots_market_id"), "odds_snapshots", ["market_id"], unique=False)
    op.create_index(op.f("ix_odds_snapshots_market_key"), "odds_snapshots", ["market_key"], unique=False)
    op.create_foreign_key("fk_odds_snapshots_odds_event_id", "odds_snapshots", "odds_events", ["odds_event_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_odds_snapshots_raw_payload_id", "odds_snapshots", "raw_api_payloads", ["raw_payload_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_odds_snapshots_bookmaker_id", "odds_snapshots", "bookmakers", ["bookmaker_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_odds_snapshots_market_id", "odds_snapshots", "markets", ["market_id"], ["id"], ondelete="SET NULL")

    op.create_table(
        "odds_market_summaries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("odds_event_id", sa.String(), nullable=False),
        sa.Column("match_id", sa.String(), nullable=True),
        sa.Column("market_key", sa.String(), nullable=False),
        sa.Column("selection_name", sa.String(), nullable=False),
        sa.Column("point", sa.Float(), nullable=True),
        sa.Column("best_odd", sa.Float(), nullable=False),
        sa.Column("average_odd", sa.Float(), nullable=False),
        sa.Column("median_odd", sa.Float(), nullable=False),
        sa.Column("lowest_odd", sa.Float(), nullable=False),
        sa.Column("bookmaker_count", sa.Integer(), nullable=False),
        sa.Column("market_spread", sa.Float(), nullable=False),
        sa.Column("raw_implied_probability", sa.Float(), nullable=False),
        sa.Column("devig_probability", sa.Float(), nullable=True),
        sa.Column("market_margin", sa.Float(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["odds_event_id"], ["odds_events.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_odds_market_summaries_odds_event_id"), "odds_market_summaries", ["odds_event_id"], unique=False)
    op.create_index(op.f("ix_odds_market_summaries_match_id"), "odds_market_summaries", ["match_id"], unique=False)
    op.create_index(op.f("ix_odds_market_summaries_market_key"), "odds_market_summaries", ["market_key"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_odds_market_summaries_market_key"), table_name="odds_market_summaries")
    op.drop_index(op.f("ix_odds_market_summaries_match_id"), table_name="odds_market_summaries")
    op.drop_index(op.f("ix_odds_market_summaries_odds_event_id"), table_name="odds_market_summaries")
    op.drop_table("odds_market_summaries")
    op.drop_constraint("fk_odds_snapshots_market_id", "odds_snapshots", type_="foreignkey")
    op.drop_constraint("fk_odds_snapshots_bookmaker_id", "odds_snapshots", type_="foreignkey")
    op.drop_constraint("fk_odds_snapshots_raw_payload_id", "odds_snapshots", type_="foreignkey")
    op.drop_constraint("fk_odds_snapshots_odds_event_id", "odds_snapshots", type_="foreignkey")
    op.drop_index(op.f("ix_odds_snapshots_market_key"), table_name="odds_snapshots")
    op.drop_index(op.f("ix_odds_snapshots_market_id"), table_name="odds_snapshots")
    op.drop_index(op.f("ix_odds_snapshots_bookmaker_id"), table_name="odds_snapshots")
    op.drop_index(op.f("ix_odds_snapshots_odds_event_id"), table_name="odds_snapshots")
    op.alter_column("odds_snapshots", "match_id", existing_type=sa.String(), nullable=False)
    for column in [
        "created_at",
        "source_last_update",
        "implied_probability",
        "selection_name",
        "market_key",
        "market_id",
        "bookmaker_id",
        "raw_payload_id",
        "odds_event_id",
    ]:
        op.drop_column("odds_snapshots", column)
    op.drop_index(op.f("ix_odds_events_linked_match_id"), table_name="odds_events")
    op.drop_index(op.f("ix_odds_events_normalized_away_team"), table_name="odds_events")
    op.drop_index(op.f("ix_odds_events_normalized_home_team"), table_name="odds_events")
    op.drop_index(op.f("ix_odds_events_sport_key"), table_name="odds_events")
    op.drop_table("odds_events")
    op.drop_index(op.f("ix_markets_key"), table_name="markets")
    op.drop_table("markets")
    op.drop_table("bookmakers")
