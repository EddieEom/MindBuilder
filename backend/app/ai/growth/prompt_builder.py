from app.ai.growth.templates import (
    SYSTEM_TEMPLATE,
    OUTPUT_SCHEMA,
)


class PromptBuilder:

    # ======================================================
    # Public
    # ======================================================

    def build(
        self,
        evidence_map: dict,
        growth_result,
    ) -> str:

        sections = [

            self._build_system(),

            self._build_context(
                evidence_map,
            ),

            self._build_unlearning(
                growth_result.unlearning,
            ),

            self._build_relearning(
                growth_result.relearning,
            ),

            self._build_newlearning(
                growth_result.newlearning,
            ),

            self._build_output_schema(),

        ]

        return "\n\n".join(sections)

    # ======================================================
    # System
    # ======================================================

    def _build_system(
        self,
    ) -> str:

        return SYSTEM_TEMPLATE

    # ======================================================
    # Evidence
    # ======================================================

    def _build_context(
        self,
        evidence_map: dict,
    ) -> str:

        text = [
            "### Current Analysis",
            "",
        ]

        for feature in evidence_map.values():

            text.append(
                f"""
Feature : {feature['feature']}
Score : {feature['score']}
Confidence : {feature['confidence']}
Strength : {feature['strength']}
Evidence Count : {feature['evidence_count']}
""".strip()
            )

        return "\n\n".join(text)

    # ======================================================
    # Unlearning
    # ======================================================

    def _build_unlearning(
        self,
        item,
    ) -> str:

        if item is None:
            return ""

        return f"""
### Rule-based Unlearning

Title
{item["title"]}

Thinking Pattern
{item["thinking_pattern"]}

Core Belief
{item["core_belief"]}

Description
{item["description"]}
""".strip()

    # ======================================================
    # Relearning
    # ======================================================

    def _build_relearning(
        self,
        item,
    ) -> str:

        if item is None:
            return ""

        return f"""
### Rule-based Relearning

Title
{item["title"]}

Root Cause
{item["root_cause"]}

Mechanism
{item["mechanism"]}

Description
{item["description"]}
""".strip()

    # ======================================================
    # Newlearning
    # ======================================================

    def _build_newlearning(
        self,
        item,
    ) -> str:

        if item is None:
            return ""

        return f"""
### Rule-based Newlearning

Title
{item["title"]}

New Belief
{item["new_belief"]}

Action
{item["action"]}

Habit
{item["habit"]}

Description
{item["description"]}
""".strip()

    # ======================================================
    # Output Schema
    # ======================================================

    def _build_output_schema(
        self,
    ) -> str:

        return f"""
### Output

반드시 아래 JSON 형식으로 출력한다.

{OUTPUT_SCHEMA}
""".strip()