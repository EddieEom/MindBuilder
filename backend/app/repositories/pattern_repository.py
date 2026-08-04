from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.feature_extractor.constants import (
    CREATIVITY,
    EXECUTION,
    FUTURE,
    PERFECTIONISM,
    RESILIENCE,
    UNCERTAINTY,
)
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)
from app.models.analysis import PatternAnalysis
from app.models.scan import Scan


PATTERN_SCORE_FIELDS = (
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

    async def get_latest_by_scan(
        self,
        scan_id: int,
    ) -> PatternAnalysis | None:

        stmt = (
            select(PatternAnalysis)
            .where(
                PatternAnalysis.scan_id == scan_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_latest_pattern(
        self,
        user_id: int,
    ) -> PatternAnalysis | None:

        stmt = (
            select(PatternAnalysis)
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
            .order_by(
                PatternAnalysis.created_at.desc(),
                PatternAnalysis.pattern_id.desc(),
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_recent_patterns(
        self,
        user_id: int,
        limit: int = 30,
    ) -> list[PatternAnalysis]:

        safe_limit = max(
            1,
            min(
                limit,
                365,
            ),
        )

        stmt = (
            select(PatternAnalysis)
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
            .order_by(
                PatternAnalysis.created_at.desc(),
                PatternAnalysis.pattern_id.desc(),
            )
            .limit(safe_limit)
        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    async def get_pattern_average(
        self,
        user_id: int,
        limit: int = 30,
    ) -> dict[str, float]:

        patterns = await self.get_recent_patterns(
            user_id=user_id,
            limit=limit,
        )

        return self._calculate_average(
            patterns
        )

    async def get_pattern_trend(
        self,
        user_id: int,
        limit: int = 30,
    ) -> dict[str, float]:

        patterns = await self.get_recent_patterns(
            user_id=user_id,
            limit=limit,
        )

        if len(patterns) < 2:

            return {
                field: 0.0
                for field in PATTERN_SCORE_FIELDS
            }

        ordered_patterns = list(
            reversed(patterns)
        )

        split_index = len(
            ordered_patterns
        ) // 2

        older_patterns = ordered_patterns[
            :split_index
        ]

        newer_patterns = ordered_patterns[
            split_index:
        ]

        older_average = self._calculate_average(
            older_patterns
        )

        newer_average = self._calculate_average(
            newer_patterns
        )

        return {
            field: round(
                newer_average[field]
                -
                older_average[field],
                2,
            )
            for field in PATTERN_SCORE_FIELDS
        }

    async def get_pattern_count(
        self,
        user_id: int,
    ) -> int:

        stmt = (
            select(
                func.count(
                    PatternAnalysis.pattern_id
                )
            )
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return int(
            result.scalar_one()
            or
            0
        )

    def _calculate_average(
        self,
        patterns: list[PatternAnalysis],
    ) -> dict[str, float]:

        if not patterns:

            return {
                field: 0.0
                for field in PATTERN_SCORE_FIELDS
            }

        return {
            field: round(
                sum(
                    self._get_score(
                        pattern,
                        field,
                    )
                    for pattern in patterns
                )
                /
                len(patterns),
                2,
            )
            for field in PATTERN_SCORE_FIELDS
        }

    def _get_score(
        self,
        pattern: PatternAnalysis,
        field: str,
    ) -> float:

        return float(
            getattr(
                pattern,
                field,
                0,
            )
            or
            0
        )
