from app.ai.feature_extractor.constants import (
    FEATURE_KEYS,
    WEIGHT_SCORE,
    TOP_PATTERN_COUNT
)

from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)

from app.ai.feature_extractor.option_rules import (
    OPTION_RULES,
    
)

from app.ai.feature_extractor.cross_rules import (
    REINFORCEMENT_RULES,
    CONFLICT_RULES,
    CONFIDENCE_RULES,
    INTERPRETATION_RULES,
)
from app.ai.feature_extractor.rule_policy import RuleQualityPolicy, RULESET_VERSION

class FeatureExtractor:

    def extract_features(
        self,
        answers: list,
    ) -> FeatureResult:

        result = FeatureResult()

        self._initialize_result(result)

        self._apply_option_rules(
            answers,
            result,
        )

        self._apply_reinforcement_rules(result)

        self._apply_conflict_rules(result)

        self._interpret_patterns(result)

        self._calculate_confidence(result)
        
        self._finalize(result)

        return result

    # ======================================================
    # Initialize
    # ======================================================

    def _initialize_result(
        self,
        result: FeatureResult,
    ) -> None:

        result.initialize_scores(FEATURE_KEYS)

    # ======================================================
    # Priority
    # ======================================================

    def _sort_rules_by_priority(
        self,
        rules: list[dict],
    ) -> list[dict]:

        return sorted(
            rules,
            key=lambda x: x.get("priority", 0),
            reverse=True,
        )

    # ======================================================
    # Option Rules
    # ======================================================

    def _apply_option_rules(
        self,
        answers: list,
        result: FeatureResult,
    ) -> None:

        for answer in answers:

            result.add_selected_option(
                answer.option_id
            )
            result.add_selected_question(
                answer.question_id
            )

            question_rules = OPTION_RULES.get(
                answer.question_id
            )

            if question_rules is None:
                continue

            rules = question_rules.get(
                answer.option_id,
                [],
            )

            rules = self._sort_rules_by_priority(
                rules
            )

            for rule in rules:

                self._apply_option_rule(
                    result,
                    rule,
                    answer.question_id,
                )

    # ======================================================
    # Apply Option Rule
    # ======================================================
    
    def _apply_option_rule(
        self,
        result: FeatureResult,
        rule: dict,
        question_id: int,
    ) -> None:

        score = WEIGHT_SCORE[
            rule["weight"]
        ]

        if rule.get("direction") == "negative":

            score *= -1

        feature = rule["feature"]

        result.add_score(
            feature,
            score,
        )

        calibrated = RuleQualityPolicy.option(
            question_id, feature, rule.get("confidence", 0.0)
        )
        result.add_confidence(feature, calibrated.confidence, calibrated.evidence_group)

        result.add_evidence(
            feature,
            {
                "rule_id": rule["rule_id"],
                "weight": rule["weight"],
                "score": score,
                "reason": rule["reason"],
                "category": rule.get("category"),
                "psychology": rule.get(
                    "psychology",
                    [],
                ),
                "confidence": calibrated.confidence,
                "raw_confidence": calibrated.raw_confidence,
                "evidence_group": calibrated.evidence_group,
                "source_type": calibrated.source_type,
                "rule_version": calibrated.rule_version,
                "direction": rule.get(
                    "direction",
                    "positive",
                ),
                "source": rule.get(
                    "source",
                    [],
                ),
            },
        )

        result.add_rule(
            {
                "rule_id": rule["rule_id"],
                "type": "option",
                "feature": feature,
                "score": score,
                "evidence_group": calibrated.evidence_group,
                "rule_version": RULESET_VERSION,
            }
        )

    # ======================================================
    # Reinforcement
    # ======================================================

    def _apply_reinforcement_rules(
        self,
        result: FeatureResult,
    ) -> None:

        for rule in REINFORCEMENT_RULES:

            if all(
                option in result.selected_options
                for option in rule["conditions"]
            ):

                result.add_score(
                    rule["feature"],
                    rule["bonus"],
                )

                calibrated = RuleQualityPolicy.reinforcement(
                    rule["rule_id"], rule["feature"], len(rule["conditions"])
                )
                result.add_confidence(
                    rule["feature"], calibrated.confidence, calibrated.evidence_group
                )

                result.add_rule(
                    {
                        "rule_id": rule["rule_id"],
                        "type": "reinforcement",
                        "feature": rule["feature"],
                        "score": rule["bonus"],
                        "evidence_group": calibrated.evidence_group,
                        "rule_version": RULESET_VERSION,
                    }
                )

                result.add_evidence(
                    rule["feature"],
                    {
                        "rule_id": rule["rule_id"],
                        "reason": rule["reason"],
                        "bonus": rule["bonus"],
                        "type": "reinforcement",
                        "confidence": calibrated.confidence,
                        "raw_confidence": calibrated.raw_confidence,
                        "evidence_group": calibrated.evidence_group,
                        "source_type": calibrated.source_type,
                        "rule_version": calibrated.rule_version,
                    },
                )

    # ======================================================
    # Conflict
    # ======================================================

    def _apply_conflict_rules(
        self,
        result: FeatureResult,
    ) -> None:

        for rule in CONFLICT_RULES:

            if not all(
                option in result.selected_options
                for option in rule["current"]
            ):
                continue

            if rule["target"] not in result.selected_options:
                continue

            conflict = {

                "rule_id": rule["rule_id"],

                "gap": rule["gap"],

                "severity": rule["severity"],

                "reason": rule["reason"],

                "current": rule["current"],

                "target": rule["target"],
                "rule_version": RULESET_VERSION,
            }

            result.add_conflict(conflict)

            result.add_rule(
                {
                    "rule_id": rule["rule_id"],
                    "type": "conflict",
                    "feature": rule["gap"],
                    "severity": rule["severity"],
                }
            )

    # ======================================================
    # Interpretation
    # ======================================================

    def _interpret_patterns(
        self,
        result: FeatureResult,
    ) -> None:

        def check_condition(condition):

            value = result.get_score(
                condition["feature"]
            )

            op = condition["operator"]

            target = condition["value"]

            if op == ">=":
                return value >= target

            if op == "<=":
                return value <= target

            if op == ">":
                return value > target

            if op == "<":
                return value < target

            if op == "==":
                return value == target

            return False

        for rule in INTERPRETATION_RULES:

            conditions = [
                check_condition(c)
                for c in rule["conditions"]
            ]

            matched = (
                all(conditions)
                if rule.get("logic") == "AND"
                else any(conditions)
            )

            if not matched:
                continue

            raw_confidence = float(rule.get("confidence", 0.0))
            pattern_confidence = RuleQualityPolicy.pattern(
                raw_confidence, len(rule.get("evidence", []))
            )
            result.add_pattern(
                {
                    "rule_id": rule["rule_id"],
                    "pattern": rule["pattern"],
                    "pattern_code": rule["pattern_code"],
                    "category": rule["category"],
                    "priority": rule["priority"],
                    "confidence": pattern_confidence,
                    "raw_confidence": raw_confidence,
                    "rule_version": RULESET_VERSION,
                    "reason": rule["reason"],
                    "evidence": rule["evidence"],
                    "psychology": rule["psychology"],
                    "source": rule["source"],
                    "tags": rule["tags"],
                    "growth_candidates": rule["growth_candidates"],
                    "identity_candidates": rule["identity_candidates"],
                    "os_candidates": rule["os_candidates"],
                }
            )

    # ======================================================
    # Confidence
    # ======================================================

    def _calculate_confidence(
        self,
        result: FeatureResult,
    ) -> None:

        confidence = 0

        feature_count = sum(
            1
            for score in result.scores.values()
            if score != 0
        )

        total_score = sum(
            abs(score)
            for score in result.scores.values()
        )

        single_feature_ratio = 0

        if total_score > 0:

            dominant_score = max(
                abs(score)
                for score in result.scores.values()
            )

            single_feature_ratio = dominant_score / total_score

        reinforcement_count = sum(
            1
            for rule in result.matched_rules
            if rule["type"] == "reinforcement"
        )

        other_count = len(
            result.selected_options.intersection(
                {16, 26, 34, 42, 51}
            )
        )

        none_count = len(
            result.selected_options.intersection(
                {15, 25, 50}
            )
        )

        for rule in CONFIDENCE_RULES:

            # Reinforcement
            if rule.get("requires_reinforcement"):

                if reinforcement_count >= 1:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            elif rule.get("requires_triple_reinforcement"):

                if reinforcement_count >= 3:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Conflict
            elif rule.get("requires_conflict"):

                if result.conflicts:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Required Questions
            elif "required_questions" in rule:

                if all(
                    q in result.selected_questions
                    for q in rule["required_questions"]
                ):
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Feature Count
            elif "min_features" in rule:

                if feature_count >= rule["min_features"]:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            elif "max_features" in rule:

                if feature_count <= rule["max_features"]:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Other
            elif rule.get("threshold") and 16 in rule.get("selected_options", []):

                if other_count >= rule["threshold"]:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # None
            elif rule.get("threshold") and 15 in rule.get("selected_options", []):

                if none_count >= rule["threshold"]:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Pattern
            elif rule.get("no_pattern"):

                if len(result.patterns) == 0:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

            # Low information
            elif rule.get("low_information"):

                if feature_count <= 1:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )
                    

            elif "single_feature_ratio" in rule:

                if single_feature_ratio >= rule["single_feature_ratio"]:
                    confidence += rule["score_delta"]

                    print(
                        f"{rule['rule_id']} "
                        f"{rule['score_delta']} "
                        f"-> {confidence}"
                    )

        result.confidence_score = max(
            0,
            min(
                100,
                confidence,
            ),
        )

    # ======================================================
    # Finalize
    # ======================================================

    def _finalize(
        self,
        result: FeatureResult,
    ) -> None:

        result.confidence_score = max(
            0,
            min(
                100,
                result.confidence_score,
            ),
        )

        for feature,value in result.scores.items():

            result.scores[feature]=max(
                0,
                min(
                    100,
                    value,
                ),
            )
            
        result.patterns.sort(
            key=lambda x:x.get(
                "priority",
                0,
            ),
            reverse=True,
        )

        result.patterns = result.patterns[
            :TOP_PATTERN_COUNT
        ]
