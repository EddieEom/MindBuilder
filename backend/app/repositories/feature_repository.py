from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.models.scan import FeatureObservation, FeatureValue, Scan

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
                confidence_score=result.get_confidence(feature_code),
                calculation_version="quality_v2",
            )

            self.db.add(feature)

            feature_values.append(feature)

            for evidence in result.evidences.get(feature_code, []):
                self.db.add(FeatureObservation(
                    scan_id=scan_id,
                    feature_code=feature_code,
                    observation_type="EVIDENCE",
                    rule_id=evidence.get("rule_id"),
                    strength=float(evidence.get("confidence") or result.get_confidence(feature_code) or 0),
                    direction=evidence.get("direction"),
                    payload=evidence,
                ))

        for conflict in result.conflicts:
            self.db.add(FeatureObservation(
                scan_id=scan_id,
                feature_code=str(conflict.get("gap") or "cross_feature"),
                observation_type="CONFLICT",
                rule_id=conflict.get("rule_id"),
                strength=self._conflict_strength(conflict.get("severity")),
                direction=None,
                payload=conflict,
            ))

        await self.db.flush()

        return feature_values

    async def quality_metrics(self, scan_id: int, user_id: int) -> dict[str, float]:
        current = list((await self.db.execute(
            select(FeatureValue).where(FeatureValue.scan_id == scan_id)
        )).scalars().all())
        evidence_count = int((await self.db.execute(
            select(func.count()).select_from(FeatureObservation).where(
                FeatureObservation.scan_id == scan_id,
                FeatureObservation.observation_type == "EVIDENCE",
            )
        )).scalar_one() or 0)
        conflict_strength = float((await self.db.execute(
            select(func.coalesce(func.sum(FeatureObservation.strength), 0)).where(
                FeatureObservation.scan_id == scan_id,
                FeatureObservation.observation_type == "CONFLICT",
            )
        )).scalar_one() or 0)
        supported = [row for row in current if float(row.feature_value) != 0]
        evidence_strength = (
            sum(float(row.confidence_score) for row in supported) / len(supported)
            if supported else 0.0
        )
        previous_scan_id = (await self.db.execute(
            select(Scan.scan_id).where(
                Scan.user_id == user_id,
                Scan.status == "COMPLETED",
                Scan.scan_id != scan_id,
            ).order_by(Scan.completed_at.desc()).limit(1)
        )).scalar_one_or_none()
        stability = 0.4
        if previous_scan_id is not None:
            previous = list((await self.db.execute(
                select(FeatureValue).where(FeatureValue.scan_id == previous_scan_id)
            )).scalars().all())
            previous_by_code = {row.feature_code: float(row.feature_value) for row in previous}
            comparisons = [
                1.0 - min(abs(float(row.feature_value) - previous_by_code[row.feature_code]) / 100.0, 1.0)
                for row in current if row.feature_code in previous_by_code
            ]
            if comparisons:
                stability = sum(comparisons) / len(comparisons)
        return {
            "evidence_count": float(evidence_count),
            "evidence_strength": evidence_strength,
            "conflict_strength": min(conflict_strength, 1.0),
            "stability": stability,
        }

    @staticmethod
    def _conflict_strength(severity) -> float:
        if isinstance(severity, (int, float)):
            return min(max(float(severity), 0.0), 1.0)
        return {"LOW": 0.25, "MEDIUM": 0.5, "HIGH": 1.0}.get(str(severity).upper(), 0.5)

    async def count_by_scan_id(
        self,
        scan_id: int,
    ) -> int:
        stmt = (
            select(func.count())
            .select_from(FeatureValue)
            .where(
                FeatureValue.scan_id == scan_id,
                FeatureValue.feature_value != 0,
            )
        )

        result = await self.db.execute(stmt)

        return int(result.scalar_one() or 0)

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
