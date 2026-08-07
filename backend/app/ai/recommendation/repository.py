from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import Recommendation
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