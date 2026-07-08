from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import PatternAnalysis
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.feature_extractor.constants import (
    FUTURE,
    CREATIVITY,
    EXECUTION,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
)

class PatternRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def commit(
        self,
    ) -> None:

        await self.db.commit()

    async def rollback(
        self,
    ) -> None:

        await self.db.rollback()

    async def create(
        self,
        scan_id: int,
        result: FeatureResult,
    ) -> PatternAnalysis:

        pattern = PatternAnalysis(

            scan_id=scan_id,

            future_score=result.get_score(FUTURE),

            creativity_score=result.get_score(CREATIVITY),

            execution_score=result.get_score(EXECUTION),

            uncertainty_score=result.get_score(UNCERTAINTY),

            perfectionism_score=result.get_score(PERFECTIONISM),

            resilience_score=result.get_score(RESILIENCE),

            confidence=result.confidence_score,

            model_version="seed_v1",
        )

        self.db.add(pattern)

        await self.db.flush()

        await self.db.refresh(pattern)

        return pattern