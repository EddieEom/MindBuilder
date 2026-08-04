"""add unique constraint to feedback growth_analysis

Revision ID: d711dfca53a0
Revises: c4b88d987234
Create Date: 2026-08-05 05:52:14.206413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd711dfca53a0'
down_revision: Union[str, None] = 'c4b88d987234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_unique_constraint(
        "uq_feedback_growth_analysis",
        "feedbacks",
        ["growth_analysis_id"],
    )


def downgrade():

    op.drop_constraint(
        "uq_feedback_growth_analysis",
        "feedbacks",
        type_="unique",
    )
