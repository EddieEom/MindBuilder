from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.growth import (
    GrowthAnalysis,
    GrowthItem,
    AIExplanation,
    Feedback,
)


class GrowthRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    # ======================================================
    # Growth Analysis
    # ======================================================

    async def create_growth_analysis(
        self,
        growth_analysis: GrowthAnalysis,
    ) -> GrowthAnalysis:

        self.db.add(
            growth_analysis
        )

        await self.db.flush()

        await self.db.refresh(
            growth_analysis
        )

        return growth_analysis

    async def get_growth_analysis(
        self,
        growth_analysis_id: int,
    ) -> GrowthAnalysis | None:

        stmt = select(
            GrowthAnalysis
        ).where(
            GrowthAnalysis.growth_analysis_id
            == growth_analysis_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    async def get_by_pattern(
        self,
        pattern_id: int,
    ) -> GrowthAnalysis | None:

        stmt = select(
            GrowthAnalysis
        ).where(
            GrowthAnalysis.pattern_id
            == pattern_id
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()

    # ======================================================
    # Growth Item
    # ======================================================

    async def create_growth_item(
        self,
        growth_item: GrowthItem,
    ) -> GrowthItem:

        self.db.add(
            growth_item
        )

        await self.db.flush()

        await self.db.refresh(
            growth_item
        )

        return growth_item

    async def get_growth_items(
        self,
        growth_analysis_id: int,
    ) -> list[GrowthItem]:

        stmt = (
            select(
                GrowthItem
            )
            .where(
                GrowthItem.growth_analysis_id
                == growth_analysis_id
            )
            .order_by(
                GrowthItem.priority.asc()
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    # ======================================================
    # AI Explanation
    # ======================================================

    async def create_ai_explanation(
        self,
        explanation: AIExplanation,
    ) -> AIExplanation:

        self.db.add(
            explanation
        )

        await self.db.flush()

        await self.db.refresh(
            explanation
        )

        return explanation

    async def get_explanations(
        self,
        growth_item_id: int,
    ) -> list[AIExplanation]:

        stmt = (
            select(
                AIExplanation
            )
            .where(
                AIExplanation.growth_item_id
                == growth_item_id
            )
            .order_by(
                AIExplanation.display_order.asc()
            )
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    # ======================================================
    # Feedback
    # ======================================================

    async def create_feedback(
        self,
        feedback: Feedback,
    ) -> Feedback:

        self.db.add(
            feedback
        )

        await self.db.flush()

        await self.db.refresh(
            feedback
        )

        return feedback

    async def get_feedbacks(
        self,
        growth_analysis_id: int,
    ) -> list[Feedback]:

        stmt = select(
            Feedback
        ).where(
            Feedback.growth_analysis_id
            == growth_analysis_id
        )

        result = await self.db.execute(
            stmt
        )

        return list(
            result.scalars().all()
        )

    # ======================================================
    # Transaction
    # ======================================================

    async def commit(
        self,
    ) -> None:

        await self.db.commit()

    async def rollback(
        self,
    ) -> None:

        await self.db.rollback()