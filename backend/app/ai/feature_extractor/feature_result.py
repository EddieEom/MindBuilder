from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FeatureResult:
    """
    Feature Extraction 결과

    Feature Extractor가 계산한 결과를
    Pattern Analysis,
    Growth Engine,
    Identity Engine에서 공통으로 사용한다.
    """

    # ==================================================
    # Feature Score
    # ==================================================

    scores: dict[str, float] = field(default_factory=dict)

    # ==================================================
    # Feature Evidence
    # ==================================================

    evidences: dict[str, list[dict[str, Any]]] = field(
        default_factory=dict
    )

    # ==================================================
    # Feature Confidence
    # ==================================================

    confidence: dict[str, float] = field(default_factory=dict)

    confidence_groups: dict[str, dict[str, float]] = field(default_factory=dict)

    # ==================================================
    # Selected Options
    # (Cross Rule 계산용)
    # ==================================================

    selected_options: set[int] = field(default_factory=set)

    # ==================================================
    # Applied Rules
    # ==================================================

    matched_rules: list[dict[str, Any]] = field(default_factory=list)

    # ==================================================
    # Conflict Result
    # ==================================================

    conflicts: list[dict[str, Any]] = field(default_factory=list)

    # ==================================================
    # Pattern Result
    # ==================================================

    patterns: list[dict[str, Any]] = field(default_factory=list)

    # ==================================================
    # Overall Confidence
    # ==================================================

    confidence_score: int = 0

    # ==================================================
    # Metadata
    # ==================================================

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==================================================
    # Warning
    # ==================================================

    warnings: list[str] = field(default_factory=list)

    selected_questions: set[int] = field(
        default_factory=set
    )
    # ==================================================
    # Methods
    # ==================================================

    def add_selected_question(
        self,
        question_id:int,
    ):

        self.selected_questions.add(question_id)

    def get_score(
        self,
        feature: str,
    ) -> float:

        return self.scores.get(
            feature,
            0,
        )
            
    def add_score(
        self,
        feature: str,
        value: float,
    ) -> None:

        self.scores[feature] = self.scores.get(feature, 0) + value

    def add_evidence(
        self,
        feature: str,
        evidence: dict[str, Any],
    ) -> None:

        self.evidences.setdefault(
            feature,
            [],
        ).append(evidence)

    def add_selected_option(
        self,
        option_id: int,
    ) -> None:

        self.selected_options.add(option_id)

    def add_rule(
        self,
        rule: dict[str, Any],
    ) -> None:

        self.matched_rules.append(rule)

    def add_conflict(
        self,
        conflict: dict[str, Any],
    ) -> None:

        self.conflicts.append(conflict)

    def add_pattern(
        self,
        pattern: dict[str, Any],
    ) -> None:

        self.patterns.append(pattern)

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)


    def initialize_scores(
        self,
        feature_keys: list[str],
    ) -> None:

        for feature in feature_keys:
            self.scores.setdefault(feature, 0)

    def get_confidence(
        self,
        feature:str,
    ):

        return self.confidence.get(
            feature,
            0,
        )

    def add_confidence(
        self,
        feature: str,
        value: float,
        evidence_group: str | None = None,
    ) -> None:
        groups = self.confidence_groups.setdefault(feature, {})
        group = evidence_group or f"LEGACY:{len(groups)}"
        bounded_value = min(max(float(value), 0.0), 1.0)
        groups[group] = max(groups.get(group, 0.0), bounded_value)
        remaining_uncertainty = 1.0
        for group_confidence in groups.values():
            remaining_uncertainty *= 1.0 - group_confidence
        self.confidence[feature] = 1.0 - remaining_uncertainty

    def set_metadata(
        self,
        key:str,
        value:Any,
    ):

        self.metadata[key]=value


    def has_option(
        self,
        option_id:int,
    ):

        return option_id in self.selected_options
    
    def has_question(
        self,
        question_id:int,
    ):

        return question_id in self.selected_questions
