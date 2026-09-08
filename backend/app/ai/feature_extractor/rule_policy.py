from dataclasses import dataclass


RULESET_VERSION = "seed_rules_v2"


@dataclass(frozen=True, slots=True)
class CalibratedRule:
    raw_confidence: float
    confidence: float
    evidence_group: str
    source_type: str
    rule_version: str = RULESET_VERSION


class RuleQualityPolicy:
    """Calibrates authored rule priors and prevents correlated evidence inflation."""

    @staticmethod
    def option(question_id: int, feature: str, raw_confidence: float) -> CalibratedRule:
        raw = RuleQualityPolicy._bound(raw_confidence)
        # A single self-report answer is useful, but never high-certainty evidence.
        calibrated = min(max(raw * 0.65, 0.20), 0.65)
        return CalibratedRule(
            raw_confidence=raw,
            confidence=calibrated,
            evidence_group=f"QUESTION:{question_id}:{feature}",
            source_type="SELF_REPORT",
        )

    @staticmethod
    def reinforcement(rule_id: str, feature: str, condition_count: int) -> CalibratedRule:
        # Cross-question agreement is independent of each individual rule, but bounded.
        calibrated = min(0.42 + max(condition_count - 2, 0) * 0.06, 0.54)
        return CalibratedRule(
            raw_confidence=calibrated,
            confidence=calibrated,
            evidence_group=f"CROSS:{rule_id}:{feature}",
            source_type="CROSS_QUESTION",
        )

    @staticmethod
    def pattern(raw_confidence: float, evidence_count: int) -> float:
        raw = RuleQualityPolicy._bound(raw_confidence)
        coverage_factor = min(0.55 + evidence_count * 0.10, 0.80)
        return min(raw * coverage_factor, 0.80)

    @staticmethod
    def _bound(value: float) -> float:
        return min(max(float(value or 0.0), 0.0), 1.0)
