from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import FeatureValue

from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.feature_extractor.constants import (
    FEATURE_KEYS,
)


class FeatureRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ======================================================
    # Feature 저장
    # ======================================================

    async def create(
        self,
        scan_id: int,
        result: FeatureResult,
    ) -> list[FeatureValue]:

        feature_values: list[FeatureValue] = []

        for feature_code in FEATURE_KEYS:

            feature = FeatureValue(

                scan_id=scan_id,

                feature_code=feature_code,

                feature_name=feature_code,

                feature_value=result.get_score(
                    feature_code
                ),
            )

            self.db.add(feature)

            feature_values.append(feature)

        await self.db.flush()

        return feature_values

    # ======================================================
    # Commit
    # ======================================================

    async def commit(
        self,
    ):

        await self.db.commit()

    # ======================================================
    # Rollback
    # ======================================================

    async def rollback(
        self,
    ):

        await self.db.rollback()