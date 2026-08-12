from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Recommendation, PatternAnalysis
from app.models.scan import Scan
from app.models.growth import NextAction

from app.ai.recommendation.result import RecommendationResult


class RecommendationRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def save(
        self,
        user_id: int,
        pattern_id: int,
        result: RecommendationResult,
    ) -> None:
        try:
            for recommendation in result.recommendations:
                model = Recommendation(
                    pattern_id=pattern_id,
                    title=recommendation.title,
                    description=recommendation.description,
                    priority=recommendation.priority,
                    status="WAITING",
                )

                self.db.add(model)
                await self.db.flush()

                for action in recommendation.actions:
                    self.db.add(
                        NextAction(
                            user_id=user_id,
                            recommendation_id=model.recommendation_id,
                            title=action.title,
                            description=action.description,
                            status="WAITING",
                        )
                    )

            await self.db.commit()

        except Exception:
            await self.db.rollback()
            raise

    async def get_current_recommendations(
        self,
        user_id: int,
        pattern_id: int,
    ) -> list[Recommendation]:
        stmt = (
            select(Recommendation)
            .join(
                PatternAnalysis,
                Recommendation.pattern_id == PatternAnalysis.pattern_id,
            )
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id,
                Recommendation.pattern_id == pattern_id,
            )
            .options(selectinload(Recommendation.next_actions))
            .order_by(
                Recommendation.priority.asc(),
                Recommendation.created_at.desc(),
            )
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())