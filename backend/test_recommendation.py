import asyncio

from app.ai.llm.client import LLMClient

from app.ai.recommendation.prompt import (
    FULL_SYSTEM_PROMPT,
    build_user_prompt,
)
from typing import cast
from app.ai.recommendation.schemas import (
    RecommendationOutputSchema,
)


async def main():

    client = LLMClient()

    pattern = {
        "future_score": 4.1,
        "creativity_score": 3.8,
        "execution_score": 4.7,
        "resilience_score": 2.9,
    }

    growth = {
        "growth_items": [
            {
                "title": "회복 부족",
                "description": "휴식 없이 계속 실행하려는 경향이 있습니다.",
            },
            {
                "title": "책임 과잉",
                "description": "모든 문제를 혼자 해결하려는 사고가 있습니다.",
            },
        ]
    }

    identity = {
        "identity_name": "Builder",
        "description": "Builds systems from ideas.",
        "confidence": 0.91,
    }

    life_map = {
        "nodes": [
            {
                "title": "Execution",
                "node_type": "INTEREST",
            },
            {
                "title": "Systems",
                "node_type": "VALUE",
            },
            {
                "title": "Iteration",
                "node_type": "GOAL",
            },
        ]
    }

    user_prompt = build_user_prompt(

        pattern=pattern,

        growth=growth,

        identity=identity,

        life_map=life_map,

    )

    response = await client.generate(

        system=FULL_SYSTEM_PROMPT,

        user=user_prompt,

        schema=RecommendationOutputSchema,

        profile="recommendation",

    )



    result = cast(
        RecommendationOutputSchema,
        response.validated,
    )

    print("=" * 80)
    print("RAW")
    print("=" * 80)
    print(response.raw_text)

    print()

    print("=" * 80)
    print("PARSED")
    print("=" * 80)
    print(response.parsed)

    print()

    print("=" * 80)
    print("VALIDATED")
    print("=" * 80)
    print(result)

    print()

    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    for index, recommendation in enumerate(
        result.recommendations,
        start=1,
    ):

        print(f"\n[{index}]")

        print("Title")
        print(recommendation.title)

        print()

        print("Description")
        print(recommendation.description)

        print()

        print("Priority")
        print(recommendation.priority)

        print()

        print("Actions")

        for action in recommendation.actions:

            print(f"  • {action.title}")
            print(f"    {action.description}")

    print()

    print("=" * 80)
    print("CONFIDENCE")
    print("=" * 80)
    print(result.confidence)

    print()

    print("=" * 80)
    print("METADATA")
    print("=" * 80)
    print(response.metadata)


if __name__ == "__main__":

    asyncio.run(main())