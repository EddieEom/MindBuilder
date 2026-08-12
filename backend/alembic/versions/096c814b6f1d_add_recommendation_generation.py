"""add recommendation generation

Revision ID: 096c814b6f1d
Revises: d711dfca53a0
Create Date: 2026-08-12 16:56:00.790343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '096c814b6f1d'
down_revision: Union[str, None] = 'd711dfca53a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Recommendation Generation 테이블 생성
    op.create_table(
        "recommendation_generations",

        sa.Column(
            "generation_id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "pattern_id",
            sa.BigInteger(),
            nullable=False,
        ),

        sa.Column(
            "confidence",
            sa.Numeric(5, 2),
            nullable=False,
        ),

        sa.Column(
            "version",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint(
            "generation_id"
        ),

        sa.ForeignKeyConstraint(
            ["pattern_id"],
            ["pattern_analysis.pattern_id"],
            ondelete="CASCADE",
            name="fk_recommendation_generation_pattern",
        ),
    )

    op.create_index(
        "ix_recommendation_generations_pattern_id",
        "recommendation_generations",
        ["pattern_id"],
    )

    # 2. 기존 recommendations에 generation_id 추가
    #
    # 기존 데이터가 존재할 수 있으므로
    # 처음에는 nullable=True로 추가한다.
    op.add_column(
        "recommendations",
        sa.Column(
            "generation_id",
            sa.BigInteger(),
            nullable=True,
        ),
    )

    op.create_index(
        "ix_recommendations_generation_id",
        "recommendations",
        ["generation_id"],
    )

    op.create_foreign_key(
        "fk_recommendations_generation",
        "recommendations",
        "recommendation_generations",
        ["generation_id"],
        ["generation_id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_recommendations_generation",
        "recommendations",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_recommendations_generation_id",
        table_name="recommendations",
    )

    op.drop_column(
        "recommendations",
        "generation_id",
    )

    op.drop_index(
        "ix_recommendation_generations_pattern_id",
        table_name="recommendation_generations",
    )

    op.drop_table(
        "recommendation_generations",
    )