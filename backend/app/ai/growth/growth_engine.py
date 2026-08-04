from app.ai.feature_extractor import feature_result
from app.ai.growth.growth_result import (
    GrowthResult,
)

from app.ai.growth.unlearning_rules import (
    UNLEARNING_RULES,
)

from app.ai.growth.relearning_rules import (
    RELEARNING_RULES,
)

from app.ai.growth.newlearning_rules import (
    NEWLEARNING_RULES,
)


class GrowthEngine:

    # ======================================================
    # Public
    # ======================================================

    def analyze(
        self,
        evidence_map: dict,
    ) -> GrowthResult:

        result = GrowthResult()

        unlearning = self._find_best_rule(
            evidence_map,
            UNLEARNING_RULES,
        )

        relearning = self._find_best_rule(
            evidence_map,
            RELEARNING_RULES,
        )

        newlearning = self._find_best_rule(
            evidence_map,
            NEWLEARNING_RULES,
        )

        if unlearning:
            result.set_unlearning(unlearning)

        if relearning:
            result.set_relearning(relearning)

        if newlearning:
            result.set_newlearning(newlearning)

            # ==========================================
            # Recommendation 생성
            # ==========================================

            result.add_recommendation(

                {

                    "title": newlearning["action"],

                    "description": newlearning["habit"],

                    "priority": 1,

                }

            )
            
        result.set_metadata(
            "rule_based",
            True,
        )

        result.set_metadata(
            "engine_version",
            "growth_rule_v1",
        )

        return result

    # ======================================================
    # Private
    # ======================================================

    def _find_best_rule(
        self,
        evidence_map: dict,
        rules: list,
    ):

        candidates = []

        for rule in rules:

            feature = evidence_map.get(
                rule.feature,
            )

            if feature is None:
                continue

            score = feature["score"]

            if not (
                rule.min_score
                <= score
                <= rule.max_score
            ):
                continue

            candidates.append(
                (
                    rule.priority,
                    feature["strength"],
                    feature,
                    rule,
                )
            )

        if not candidates:
            return None

        candidates.sort(
            key=lambda x: (
                x[0],
                x[1],
            ),
            reverse=True,
        )

        _, _, feature, rule = candidates[0]

        return self._build_result(
            rule,
            feature,
        )

    # ======================================================
    # Build Result
    # ======================================================

    def _build_result(
        self,
        rule,
        feature: dict,
    ) -> dict:

        result = {

            "rule_id": rule.rule_id,

            "feature": rule.feature,

            "title": rule.title,

            "score": feature["score"],

            "confidence": feature["confidence"],

            "strength": feature["strength"],

            "evidences": feature["evidences"],

        }

        if hasattr(
            rule,
            "thinking_pattern",
        ):
            result["thinking_pattern"] = (
                rule.thinking_pattern
            )

        if hasattr(
            rule,
            "core_belief",
        ):
            result["core_belief"] = (
                rule.core_belief
            )

        if hasattr(
            rule,
            "root_cause",
        ):
            result["root_cause"] = (
                rule.root_cause
            )

        if hasattr(
            rule,
            "mechanism",
        ):
            result["mechanism"] = (
                rule.mechanism
            )

        if hasattr(
            rule,
            "new_belief",
        ):
            result["new_belief"] = (
                rule.new_belief
            )

        if hasattr(
            rule,
            "action",
        ):
            result["action"] = (
                rule.action
            )

        if hasattr(
            rule,
            "habit",
        ):
            result["habit"] = (
                rule.habit
            )

        if hasattr(
            rule,
            "description",
        ):
            result["description"] = (
                rule.description
            )

        if hasattr(
            rule,
            "psychology",
        ):
            result["psychology"] = (
                rule.psychology
            )

        return result

    # ======================================================
    # Future
    # ======================================================

    def analyze_by_llm(
        self,
        evidence_map: dict,
    ):

        raise NotImplementedError(
            "LLM Engine will be implemented later."
        )