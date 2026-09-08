"""add user settings

Revision ID: 7f4a1b2c3d4e
Revises: 096c814b6f1d
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "7f4a1b2c3d4e"
down_revision: Union[str, None] = "096c814b6f1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("dark_mode", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("language", sa.String(length=10), server_default="ko", nullable=False),
        sa.Column("notifications_enabled", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("reminder_hour", sa.Integer(), server_default="20", nullable=False),
        sa.Column("timezone", sa.String(length=64), server_default="Asia/Seoul", nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("user_settings")
