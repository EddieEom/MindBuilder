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
    NewlearningResponse,
    RelearningResponse,
    GrowthResponse,
    UnlearningResponse,
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

            unlearning=(
                UnlearningResponse(
                    **growth_result.unlearning
                )
                if growth_result.unlearning
                else None
            ),

            relearning=(
                RelearningResponse(
                    **growth_result.relearning
                )
                if growth_result.relearning
                else None
            ),

            newlearning=(
                NewlearningResponse(
                    **growth_result.newlearning
                )
                if growth_result.newlearning
                else None
            ),

            explanations=growth_result.explanations,

            recommendations=growth_result.recommendations,

            feedback=growth_result.feedback,

            metadata=growth_result.metadata,

            warnings=growth_result.warnings,
        )
