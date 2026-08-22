
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.growth import (
    GrowthAnalysis,
    GrowthItem,
    GrowthItemType,
    ExplanationType,
    AIExplanation,
    Feedback,
    NextAction,
)
from app.models.analysis import (
    RecommendationGeneration,
    Recommendation,
    PatternAnalysis,
)

class GrowthRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db




    # ======================================================
    # Recommendation
    # ======================================================

    async def get_recommendations(
        self,
        pattern_id: int,
    ) -> list[Recommendation]:

        stmt = (
            select(Recommendation)
            .where(
                Recommendation.pattern_id == pattern_id
            )
            .order_by(
                Recommendation.priority.asc()
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def create_recommendation_generation(
        self,
        generation: RecommendationGeneration,
    ) -> RecommendationGeneration:
        self.db.add(generation)

        await self.db.flush()
        await self.db.refresh(generation)

        return generation

    async def create_recommendation(
        self,
        recommendation: Recommendation,
    ) -> Recommendation:
        self.db.add(recommendation)

        await self.db.flush()
        await self.db.refresh(recommendation)

        return recommendation

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
            .options(
                selectinload(
                    GrowthItem.growth_item_type
                )
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
    # Growth Item Type
    # ======================================================

    async def get_or_create_growth_item_type(
        self,
        type_name: str,
        display_order: int = 1,
        description: str | None = None,
    ):

        stmt = (
            select(
                GrowthItemType
            )
            .where(
                GrowthItemType.type_name == type_name
            )
        )

        result = await self.db.execute(stmt)

        item_type = result.scalar_one_or_none()

        if item_type is not None:
            return item_type

        item_type = GrowthItemType(
            type_name=type_name,
            display_order=display_order,
            description=description,
        )

        self.db.add(item_type)

        await self.db.flush()

        await self.db.refresh(item_type)

        return item_type

    # ======================================================
    # Explanation Type
    # ======================================================

    async def get_or_create_explanation_type(
        self,
        type_code: str,
        type_name: str,
        display_order: int = 1,
        description: str | None = None,
    ):

        stmt = (
            select(
                ExplanationType
            )
            .where(
                ExplanationType.type_code == type_code
            )
        )

        result = await self.db.execute(stmt)

        explanation_type = result.scalar_one_or_none()

        if explanation_type is not None:
            return explanation_type

        explanation_type = ExplanationType(
            type_code=type_code,
            type_name=type_name,
            display_order=display_order,
            description=description,
        )

        self.db.add(explanation_type)

        await self.db.flush()

        await self.db.refresh(explanation_type)

        return explanation_type

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

    async def create_next_action(
        self,
        next_action: NextAction,
    ) -> NextAction:

        self.db.add(
            next_action
        )

        await self.db.flush()

        await self.db.refresh(
            next_action
        )

        return next_action

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
    # Feedback
    # ======================================================

    async def get_feedback(
        self,
        growth_analysis_id: int,
    ) -> Feedback | None:

        stmt = (
            select(
                Feedback
            )
            .where(
                Feedback.growth_analysis_id
                == growth_analysis_id
            )
        )

        result = await self.db.execute(
            stmt
        )

        return result.scalar_one_or_none()


    async def upsert_feedback(
        self,
        growth_analysis_id: int,
        rating: int,
        comment: str | None,
    ) -> Feedback:

        feedback = await self.get_feedback(
            growth_analysis_id
        )

        if feedback is None:

            feedback = Feedback(

                growth_analysis_id=growth_analysis_id,

                rating=rating,

                comment=comment,

            )

            self.db.add(
                feedback
            )

        else:

            feedback.rating = rating

            feedback.comment = comment

        await self.db.flush()

        await self.db.refresh(
            feedback
        )

        return feedback
        
    async def get_dashboard_growth(
        self,
        user_id: int,
    ) -> GrowthAnalysis | None:

        stmt = (
            select(GrowthAnalysis)
            .join(
                PatternAnalysis,
                GrowthAnalysis.pattern_id
                == PatternAnalysis.pattern_id,
            )
            .join(
                PatternAnalysis.scan,
            )
            .where(
                PatternAnalysis.scan.has(
                    user_id=user_id
                )
            )
            .order_by(
                GrowthAnalysis.created_at.desc()
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # ======================================================
    # Current Growth
    # ======================================================

    async def get_current_growth(
        self,
        user_id: int,
    ) -> GrowthAnalysis | None:

        stmt = (
            select(GrowthAnalysis)
            .options(
                selectinload(
                    GrowthAnalysis.growth_items
                ).selectinload(
                    GrowthItem.growth_item_type
                )
            )
            .join(
                PatternAnalysis,
                GrowthAnalysis.pattern_id
                == PatternAnalysis.pattern_id,
            )
            .join(
                PatternAnalysis.scan,
            )
            .where(
                PatternAnalysis.scan.has(
                    user_id=user_id
                )
            )
            .order_by(
                GrowthAnalysis.created_at.desc()
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

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


    
