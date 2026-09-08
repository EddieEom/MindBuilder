"""add feature observations and confidence

Revision ID: a81d92e4f5b6
Revises: 7f4a1b2c3d4e
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "a81d92e4f5b6"
down_revision: Union[str, None] = "7f4a1b2c3d4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("feature_values", sa.Column("confidence_score", sa.DECIMAL(5, 4), server_default="0", nullable=False))
    op.add_column("feature_values", sa.Column("calculation_version", sa.String(30), server_default="quality_v2", nullable=False))
    op.create_table(
        "feature_observations",
        sa.Column("observation_id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("scan_id", sa.BIGINT(), nullable=False),
        sa.Column("feature_code", sa.String(100), nullable=False),
        sa.Column("observation_type", sa.String(20), nullable=False),
        sa.Column("rule_id", sa.String(100), nullable=True),
        sa.Column("strength", sa.DECIMAL(5, 4), server_default="0", nullable=False),
        sa.Column("direction", sa.String(20), nullable=True),
        sa.Column("payload", sa.JSON(), server_default="{}", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["scan_id"], ["scans.scan_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("observation_id"),
    )
    op.create_index("ix_feature_observations_scan_id", "feature_observations", ["scan_id"])
    op.create_index("ix_feature_observations_feature_code", "feature_observations", ["feature_code"])


def downgrade() -> None:
    op.drop_index("ix_feature_observations_feature_code", table_name="feature_observations")
    op.drop_index("ix_feature_observations_scan_id", table_name="feature_observations")
    op.drop_table("feature_observations")
    op.drop_column("feature_values", "calculation_version")
    op.drop_column("feature_values", "confidence_score")
