from app.ai.feature_extractor.feature_extractor import (
    FeatureExtractor,
)

from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.models.analysis import Insight


class PatternAnalysisService:

    def __init__(
        self,
        answer_repository,
        pattern_repository,
        feature_repository,
    ):

        self.answer_repository = answer_repository
        self.pattern_repository = pattern_repository
        self.feature_repository = feature_repository

        self.feature_extractor = FeatureExtractor()

    async def analyze(
        self,
        scan_id: int,
    ) -> FeatureResult:
        
        try:
            answers = await self.answer_repository.get_answers_by_scan_id(
                scan_id
            )

            if not answers:
                raise ValueError(
                    "Answer not found."
                )

            result = self.feature_extractor.extract_features(
                answers
            )

            pattern = await self.pattern_repository.create(
                scan_id=scan_id,
                result=result,
            )

            await self.feature_repository.create(
                scan_id=scan_id,
                result=result,
            )

            await self._persist_insights(
                pattern,
                result,
            )

            result.metadata["pattern_id"] = (
                pattern.pattern_id
            )

            return result

        except Exception:

            await self.pattern_repository.rollback()

            raise

    async def _persist_insights(
        self,
        pattern,
        result: FeatureResult,
    ) -> None:

        if not result.patterns:
            return

        for raw_pattern in result.patterns:
            title = raw_pattern.get("pattern", "Pattern Insight")
            content = raw_pattern.get("reason", "")
            priority = int(raw_pattern.get("priority", 1))

            await self.pattern_repository.create_insight(
                Insight(
                    pattern_id=pattern.pattern_id,
                    title=title,
                    content=content,
                    priority=priority,
                )
            )
