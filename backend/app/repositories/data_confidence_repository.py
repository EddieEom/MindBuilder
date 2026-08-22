from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import DataConfidence


class DataConfidenceRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> DataConfidence | None:
        stmt = (
            select(DataConfidence)
            .where(
                DataConfidence.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def upsert(
        self,
        user_id: int,
        scan_count: int,
        confidence_score: float,
        current_stage: str,
    ) -> DataConfidence:
        data_confidence = await self.get_by_user_id(
            user_id
        )

        if data_confidence is None:
            data_confidence = DataConfidence(
                user_id=user_id,
                scan_count=scan_count,
                confidence_score=confidence_score,
                current_stage=current_stage,
            )
            self.db.add(data_confidence)
        else:
            data_confidence.scan_count = scan_count
            data_confidence.confidence_score = confidence_score
            data_confidence.current_stage = current_stage

        await self.db.flush()
        await self.db.refresh(data_confidence)

        return data_confidence

    async def commit(
        self,
    ) -> None:
        await self.db.commit()

    async def rollback(
        self,
    ) -> None:
        await self.db.rollback()
