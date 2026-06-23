"""real football data foundation

Revision ID: 20260623_0002
Revises: 20260623_0001
Create Date: 2026-06-23
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260623_0002"
down_revision: Union[str, None] = "20260623_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "raw_api_payloads",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("endpoint", sa.String(), nullable=False),
        sa.Column("request_method", sa.String(), nullable=False),
        sa.Column("request_params_json", sa.JSON(), nullable=False),
        sa.Column("response_status", sa.Integer(), nullable=True),
        sa.Column("raw_payload_json", sa.JSON(), nullable=False),
        sa.Column("payload_hash", sa.String(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cost_estimate", sa.Float(), nullable=False),
        sa.Column("error_message", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_raw_api_payloads_provider"), "raw_api_payloads", ["provider"], unique=False)
    op.create_index(op.f("ix_raw_api_payloads_payload_hash"), "raw_api_payloads", ["payload_hash"], unique=False)

    op.create_table(
        "competitions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("external_provider", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("external_provider", "external_id", "season", name="uq_competitions_external_season"),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("normalized_name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("normalized_name", "country", name="uq_teams_normalized_country"),
    )
    op.create_index(op.f("ix_teams_normalized_name"), "teams", ["normalized_name"], unique=False)
    op.create_table(
        "team_aliases",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("team_id", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=False),
        sa.Column("external_name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider", "external_id", name="uq_team_alias_provider_external"),
    )
    op.create_index(op.f("ix_team_aliases_team_id"), "team_aliases", ["team_id"], unique=False)

    op.add_column("matches", sa.Column("competition_id", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("external_provider", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("external_id", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("home_team_id", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("away_team_id", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("home_team_name_snapshot", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("away_team_name_snapshot", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("home_score", sa.Integer(), nullable=True))
    op.add_column("matches", sa.Column("away_score", sa.Integer(), nullable=True))
    op.add_column("matches", sa.Column("raw_payload_id", sa.String(), nullable=True))
    op.add_column("matches", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f("ix_matches_competition_id"), "matches", ["competition_id"], unique=False)
    op.create_index(op.f("ix_matches_external_id"), "matches", ["external_id"], unique=False)
    op.create_index(op.f("ix_matches_home_team_id"), "matches", ["home_team_id"], unique=False)
    op.create_index(op.f("ix_matches_away_team_id"), "matches", ["away_team_id"], unique=False)
    op.create_foreign_key("fk_matches_competition_id", "matches", "competitions", ["competition_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_matches_home_team_id", "matches", "teams", ["home_team_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_matches_away_team_id", "matches", "teams", ["away_team_id"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_matches_raw_payload_id", "matches", "raw_api_payloads", ["raw_payload_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    op.drop_constraint("fk_matches_raw_payload_id", "matches", type_="foreignkey")
    op.drop_constraint("fk_matches_away_team_id", "matches", type_="foreignkey")
    op.drop_constraint("fk_matches_home_team_id", "matches", type_="foreignkey")
    op.drop_constraint("fk_matches_competition_id", "matches", type_="foreignkey")
    op.drop_index(op.f("ix_matches_away_team_id"), table_name="matches")
    op.drop_index(op.f("ix_matches_home_team_id"), table_name="matches")
    op.drop_index(op.f("ix_matches_external_id"), table_name="matches")
    op.drop_index(op.f("ix_matches_competition_id"), table_name="matches")
    for column in [
        "updated_at",
        "raw_payload_id",
        "away_score",
        "home_score",
        "away_team_name_snapshot",
        "home_team_name_snapshot",
        "away_team_id",
        "home_team_id",
        "external_id",
        "external_provider",
        "competition_id",
    ]:
        op.drop_column("matches", column)
    op.drop_index(op.f("ix_team_aliases_team_id"), table_name="team_aliases")
    op.drop_table("team_aliases")
    op.drop_index(op.f("ix_teams_normalized_name"), table_name="teams")
    op.drop_table("teams")
    op.drop_table("competitions")
    op.drop_index(op.f("ix_raw_api_payloads_payload_hash"), table_name="raw_api_payloads")
    op.drop_index(op.f("ix_raw_api_payloads_provider"), table_name="raw_api_payloads")
    op.drop_table("raw_api_payloads")
