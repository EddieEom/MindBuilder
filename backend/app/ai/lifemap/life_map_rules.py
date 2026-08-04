from dataclasses import dataclass

from app.ai.identity.identity_result import (
    IdentityResult,
)

from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.growth.growth_result import (
    GrowthResult,
)


# ==========================================================
# Evidence
# ==========================================================


@dataclass
class LifeMapEvidence:

    category: str

    title: str

    weight: float

    source: str


# ==========================================================
# Rule
# ==========================================================


@dataclass
class LifeMapRule:

    category: str

    title: str

    identity: str | None = None

    min_execution: int = 0

    min_creativity: int = 0

    min_future: int = 0

    weight: float = 1.0


# ==========================================================
# Rules
# ==========================================================


LIFE_MAP_RULES = [

    # --------------------------------------------------

    LifeMapRule(

        category="INTEREST",

        title="Programming",

        identity="탐구하는 Builder",

        min_execution=50,

        weight=0.95,

    ),

    # --------------------------------------------------

    LifeMapRule(

        category="CAREER",

        title="AI Engineer",

        identity="탐구하는 Builder",

        min_execution=60,

        weight=0.90,

    ),

    # --------------------------------------------------

    LifeMapRule(

        category="VALUE",

        title="Growth",

        identity="탐구하는 Builder",

        weight=0.85,

    ),

    # --------------------------------------------------

    LifeMapRule(

        category="GOAL",

        title="Continuous Learning",

        identity="탐구하는 Builder",

        weight=0.90,

    ),

]


class LifeMapRuleEngine:

    def evaluate(

        self,

        feature_result: FeatureResult,

        identity_result: IdentityResult,

        growth_result: GrowthResult,

    ) -> list[LifeMapEvidence]:

        evidences = []

        execution = feature_result.scores.get(

            "execution_score",

            0,

        )

        creativity = feature_result.scores.get(

            "creativity_score",

            0,

        )

        future = feature_result.scores.get(

            "future_score",

            0,

        )

        for rule in LIFE_MAP_RULES:

            if (

                rule.identity

                and

                rule.identity != identity_result.identity_name

            ):

                continue

            if execution < rule.min_execution:

                continue

            if creativity < rule.min_creativity:

                continue

            if future < rule.min_future:

                continue

            evidences.append(

                LifeMapEvidence(

                    category=rule.category,

                    title=rule.title,

                    weight=rule.weight,

                    source="rule",

                )

            )

        return evidences


