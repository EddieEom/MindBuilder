import json
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / "prompts"

SYSTEM_PROMPT = (
    PROMPT_DIR / "system_prompt.txt"
).read_text(
    encoding="utf-8"
)

RECOMMENDATION_PROMPT = (
    PROMPT_DIR / "recommendation_prompt.txt"
).read_text(
    encoding="utf-8"
)

OUTPUT_SCHEMA = (
    PROMPT_DIR / "output_schema.txt"
).read_text(
    encoding="utf-8"
)

FULL_SYSTEM_PROMPT = "\n\n".join(
    [
        SYSTEM_PROMPT,
        RECOMMENDATION_PROMPT,
        OUTPUT_SCHEMA,
    ]
)

USER_TEMPLATE = """
Pattern Analysis
================
{pattern}

Growth Analysis
===============
{growth}

Identity Analysis
=================
{identity}

LifeMap Analysis
================
{lifemap}

Generate recommendations according to the system instructions.

Rules

- Base every recommendation ONLY on the analyses above.
- Do NOT invent facts.
- Do NOT repeat the analysis.
- Produce practical recommendations.
- Produce exactly 3 recommendations.
- Produce exactly 2 next actions for each recommendation.
- NEVER produce a third next action.
- NEVER produce more than 3 recommendations.
- Return ONLY valid JSON.
- Every text field MUST contain actual Korean content.
- NEVER output placeholder values such as "string", "example", or "test".
- If the evidence is insufficient, return an empty recommendations array with confidence 0.0.

OUTPUT COUNT CONSTRAINTS

- The "recommendations" array MUST contain exactly 3 items.
- Each recommendation MUST contain exactly 2 actions.
- Never generate a third action.
- Never generate a fourth recommendation.
- Do not generate any additional fields.
- Every recommendation MUST have exactly:
  title, description, priority, actions.
- Every action MUST have exactly:
  title, description.
- Stop after completing the second action of the third recommendation.
"""


def build_user_prompt(
    *,
    pattern,
    growth,
    identity,
    life_map,
) -> str:

    return USER_TEMPLATE.format(
        pattern=json.dumps(
            pattern,
            ensure_ascii=False,
            indent=2,
        ),
        growth=json.dumps(
            growth,
            ensure_ascii=False,
            indent=2,
        ),
        identity=json.dumps(
            identity,
            ensure_ascii=False,
            indent=2,
        ),
        lifemap=json.dumps(
            life_map,
            ensure_ascii=False,
            indent=2,
        ),
    )