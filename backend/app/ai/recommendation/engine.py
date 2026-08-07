from app.ai.recommendation.prompt import (
    FULL_SYSTEM_PROMPT,
    USER_TEMPLATE,
)

from app.ai.recommendation.schemas import (
    RecommendationOutputSchema,
)

from app.ai.recommendation.result import (
    Recommendation,
    RecommendationResult,
    NextAction,
)


class RecommendationEngine:

    def __init__(self, llm):

        self.llm = llm

    async def run(

        self,

        pattern,

        growth,

        identity,

        life_map,

    ) -> RecommendationResult:

        prompt = USER_TEMPLATE.format(

            pattern=pattern,

            growth=growth,

            identity=identity,

            lifemap=life_map,

        )

        response = await self.llm.generate(

            system=FULL_SYSTEM_PROMPT,

            user=prompt,

            schema=RecommendationOutputSchema,

            profile="recommendation",

        )

        output: RecommendationOutputSchema = response.validated

        recommendations = []

        for item in output.recommendations:

            actions = [

                NextAction(

                    title=action.title,

                    description=action.description,

                )

                for action in item.actions

            ]

            recommendations.append(

                Recommendation(

                    title=item.title,

                    description=item.description,

                    priority=item.priority,

                    actions=actions,

                )

            )

        return RecommendationResult(

            recommendations=recommendations,

            confidence=output.confidence,

            version="recommendation_v1",

        )