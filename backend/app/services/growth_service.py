from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.growth.evidence_builder import (
    EvidenceBuilder,
)

from app.ai.growth.growth_engine import (
    GrowthEngine,
)

from app.schemas.growth import (
    GrowthResponse,
)


class GrowthService:

    def __init__(
        self,
    ):

        self.evidence_builder = (
            EvidenceBuilder()
        )

        self.growth_engine = (
            GrowthEngine()
        )

    async def analyze(
        self,
        feature_result: FeatureResult,
    ):

        evidence_map = (
            self.evidence_builder.build(
                feature_result
            )
        )

        growth_result = (
            self.growth_engine.analyze(
                evidence_map
            )
        )

        return GrowthResponse(

            unlearning=growth_result.unlearning,

            relearning=growth_result.relearning,

            newlearning=growth_result.newlearning,

            explanations=growth_result.explanations,

            recommendations=growth_result.recommendations,

            feedback=growth_result.feedback,

            metadata=growth_result.metadata,

            warnings=growth_result.warnings,
        )