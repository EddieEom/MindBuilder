from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import (
    Recommendation,
    RecommendationGeneration,
    PatternAnalysis,
)
from app.models.scan import Scan
from app.models.growth import NextAction

from app.ai.recommendation.result import RecommendationResult


class RecommendationRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ======================================================
    # Save Recommendation Generation
    # ======================================================

    async def save(
        self,
        user_id: int,
        pattern_id: int,
        result: RecommendationResult,
    ) -> int:

        try:
            # --------------------------------------------------
            # 1. Recommendation Generation 생성
            # --------------------------------------------------

            generation = RecommendationGeneration(
                pattern_id=pattern_id,
                confidence=result.confidence,
                version=result.version,
            )

            self.db.add(generation)

            # generation_id 확보
            await self.db.flush()

            # --------------------------------------------------
            # 2. Recommendation 생성
            # --------------------------------------------------

            for recommendation in result.recommendations:

                model = Recommendation(
                    generation_id=generation.generation_id,
                    pattern_id=pattern_id,
                    title=recommendation.title,
                    description=recommendation.description,
                    priority=recommendation.priority,
                    status="WAITING",
                )

                self.db.add(model)

                # recommendation_id 확보
                await self.db.flush()

                # --------------------------------------------------
                # 3. NextAction 생성
                # --------------------------------------------------

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

            # --------------------------------------------------
            # 4. 전체 Transaction Commit
            # --------------------------------------------------

            await self.db.commit()

            return generation.generation_id

        except Exception:
            await self.db.rollback()
            raise

    # ======================================================
    # Get Specific Recommendation Generation
    # ======================================================

    async def get_generation(
        self,
        user_id: int,
        generation_id: int,
    ) -> RecommendationGeneration | None:

        stmt = (
            select(RecommendationGeneration)
            .join(
                PatternAnalysis,
                RecommendationGeneration.pattern_id
                == PatternAnalysis.pattern_id,
            )
            .join(
                Scan,
                PatternAnalysis.scan_id
                == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id,
                RecommendationGeneration.generation_id
                == generation_id,
            )
            .options(
                selectinload(
                    RecommendationGeneration.recommendations
                ).selectinload(
                    Recommendation.next_actions
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # ======================================================
    # Get Current Recommendation Generation
    # ======================================================

    async def get_current_generation(
        self,
        user_id: int,
        pattern_id: int,
    ) -> RecommendationGeneration | None:

        stmt = (
            select(RecommendationGeneration)
            .join(
                PatternAnalysis,
                RecommendationGeneration.pattern_id
                == PatternAnalysis.pattern_id,
            )
            .join(
                Scan,
                PatternAnalysis.scan_id
                == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id,
                RecommendationGeneration.pattern_id
                == pattern_id,
            )
            .options(
                selectinload(
                    RecommendationGeneration.recommendations
                ).selectinload(
                    Recommendation.next_actions
                )
            )
            .order_by(
                RecommendationGeneration.created_at.desc(),
                RecommendationGeneration.generation_id.desc(),
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()