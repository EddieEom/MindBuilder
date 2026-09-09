"""add identity hypotheses and feedback

Revision ID: b92e03f6a7c8
Revises: a81d92e4f5b6
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "b92e03f6a7c8"
down_revision: Union[str, None] = "a81d92e4f5b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("identities", sa.Column("candidate_snapshot", sa.JSON(), server_default="[]", nullable=False))
    op.add_column("identities", sa.Column("hypothesis_status", sa.String(20), server_default="EMERGING", nullable=False))
    op.create_table(
        "identity_feedback",
        sa.Column("feedback_id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("identity_id", sa.BIGINT(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("agreement", sa.String(20), nullable=False),
        sa.Column("correction_text", sa.Text(), nullable=True),
        sa.Column("provenance", sa.String(20), server_default="USER_CLAIM", nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("agreement IN ('AGREE', 'PARTIAL', 'DISAGREE', 'UNSURE')", name="ck_identity_feedback_agreement"),
        sa.ForeignKeyConstraint(["identity_id"], ["identities.identity_id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.user_id"]),
        sa.PrimaryKeyConstraint("feedback_id"),
        sa.UniqueConstraint("identity_id", "user_id", name="uq_identity_feedback_identity_user"),
    )
    op.create_index("ix_identity_feedback_identity_id", "identity_feedback", ["identity_id"])
    op.create_index("ix_identity_feedback_user_id", "identity_feedback", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_identity_feedback_user_id", table_name="identity_feedback")
    op.drop_index("ix_identity_feedback_identity_id", table_name="identity_feedback")
    op.drop_table("identity_feedback")
    op.drop_column("identities", "hypothesis_status")
    op.drop_column("identities", "candidate_snapshot")
