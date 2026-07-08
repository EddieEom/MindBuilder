from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.question import (
    Question,
    QuestionSet,
    QuestionSetItem,
)


class QuestionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_question_set(
        self,
        target_stage: str = "SEED",
    ) -> QuestionSet | None:

        stmt = (
            select(QuestionSet)
            .where(
                QuestionSet.target_stage == target_stage,
                QuestionSet.is_active.is_(True),
            )
            .options(
                selectinload(QuestionSet.question_set_items)
                .selectinload(QuestionSetItem.question)
                .selectinload(Question.options)
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()