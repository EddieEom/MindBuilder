from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.identity.identity_result import (
    IdentityResult,
)

from app.ai.growth.growth_result import (
    GrowthResult,
)

from app.ai.lifemap.life_map_rules import (
    LifeMapRuleEngine,
    LifeMapEvidence,
)


class LifeMapBuilder:

    def __init__(self):

        self.rule_engine = LifeMapRuleEngine()

    # ======================================================
    # Build Evidence
    # ======================================================

    def build(

        self,

        feature_result: FeatureResult,

        identity_result: IdentityResult,

        growth_result: GrowthResult,

    ) -> list[LifeMapEvidence]:

        evidences = self.rule_engine.evaluate(

            feature_result=feature_result,

            identity_result=identity_result,

            growth_result=growth_result,

        )

        evidences.sort(

            key=lambda evidence: evidence.weight,

            reverse=True,

        )

        return evidences