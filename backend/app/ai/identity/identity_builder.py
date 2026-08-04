from typing import Any

from app.ai.feature_extractor.constants import (
    CREATIVITY,
    EXECUTION,
    FUTURE,
    PERFECTIONISM,
    RESILIENCE,
    UNCERTAINTY,
)
from app.ai.feature_extractor.feature_result import (
    FeatureResult,
)
from app.models.analysis import PatternAnalysis
from app.schemas.growth import (
    GrowthResponse,
)


PATTERN_SCORE_FIELDS = (
    FUTURE,
    CREATIVITY,
    EXECUTION,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
)


class IdentityBuilder:

    """
    Builds Identity evidence from Layer2 Pattern history first.

    Feature and Growth data are kept as supporting evidence, but the
    Identity score source is the accumulated Pattern layer.
    """

    def build(
        self,
        feature_result: FeatureResult,
        growth_result: GrowthResponse,
        latest_pattern: PatternAnalysis | None = None,
        recent_patterns: list[PatternAnalysis] | None = None,
        pattern_average: dict[str, float] | None = None,
        pattern_trend: dict[str, float] | None = None,
        pattern_count: int | None = None,
    ) -> dict[str, Any]:

        recent_patterns = recent_patterns or []

        pattern_history = [
            self._pattern_to_dict(pattern)
            for pattern in recent_patterns
        ]

        latest_pattern_map = (
            self._pattern_to_dict(latest_pattern)
            if latest_pattern is not None
            else (
                pattern_history[0]
                if pattern_history
                else {}
            )
        )

        normalized_average = self._normalize_scores(
            pattern_average
        )

        if not any(
            normalized_average.values()
        ) and latest_pattern_map:

            normalized_average = {
                field: latest_pattern_map.get(
                    field,
                    0.0,
                )
                for field in PATTERN_SCORE_FIELDS
            }

        normalized_trend = self._normalize_scores(
            pattern_trend
        )

        resolved_pattern_count = (
            pattern_count
            if pattern_count is not None
            else len(pattern_history)
        )

        growth_evidence = self._build_growth_evidence(
            growth_result
        )

        stable_characteristics = (
            self._build_stable_characteristics(
                pattern_history=pattern_history,
                pattern_average=normalized_average,
                pattern_trend=normalized_trend,
            )
        )

        warnings = []

        if resolved_pattern_count <= 0:

            warnings.append(
                "Identity requires Layer2 pattern history."
            )

        elif resolved_pattern_count < 3:

            warnings.append(
                "Identity confidence is limited until more Pattern history accumulates."
            )

        warnings.extend(
            feature_result.warnings
        )

        warnings.extend(
            growth_result.warnings
        )

        return {

            "source_layer": "Layer2",

            "latest_pattern": latest_pattern_map,

            "pattern_history": pattern_history,

            "pattern_average": normalized_average,

            "pattern_trend": normalized_trend,

            "pattern_count": resolved_pattern_count,

            "stable_characteristics": stable_characteristics,

            "scores": normalized_average,

            "feature": {

                "scores": dict(
                    feature_result.scores
                ),

                "confidence": dict(
                    feature_result.confidence
                ),

                "evidence": dict(
                    feature_result.evidences
                ),

                "patterns": list(
                    feature_result.patterns
                ),

            },

            "growth": {

                "unlearning": growth_result.unlearning,

                "relearning": growth_result.relearning,

                "newlearning": growth_result.newlearning,

            },

            "growth_evidence": growth_evidence,

            "explanations": list(
                growth_result.explanations
            ),

            "recommendations": list(
                growth_result.recommendations
            ),

            "metadata": {

                **feature_result.metadata,

                **growth_result.metadata,

                "source_layer": "Layer2",

                "pattern_count": resolved_pattern_count,

            },

            "warnings": warnings,

        }

    def _pattern_to_dict(
        self,
        pattern: PatternAnalysis | None,
    ) -> dict[str, Any]:

        if pattern is None:

            return {}

        return {

            "pattern_id": pattern.pattern_id,

            "scan_id": pattern.scan_id,

            "future_score": self._to_float(
                pattern.future_score
            ),

            "creativity_score": self._to_float(
                pattern.creativity_score
            ),

            "execution_score": self._to_float(
                pattern.execution_score
            ),

            "uncertainty_score": self._to_float(
                pattern.uncertainty_score
            ),

            "perfectionism_score": self._to_float(
                pattern.perfectionism_score
            ),

            "resilience_score": self._to_float(
                pattern.resilience_score
            ),

            "confidence": self._to_float(
                pattern.confidence
            ),

            "model_version": pattern.model_version,

            "created_at": pattern.created_at,

        }

    def _normalize_scores(
        self,
        scores: dict[str, float] | None,
    ) -> dict[str, float]:

        scores = scores or {}

        return {
            field: round(
                self._to_float(
                    scores.get(
                        field,
                        0.0,
                    )
                ),
                2,
            )
            for field in PATTERN_SCORE_FIELDS
        }

    def _build_growth_evidence(
        self,
        growth_result: GrowthResponse,
    ) -> dict[str, Any]:

        items = {

            "unlearning": self._model_to_dict(
                growth_result.unlearning
            ),

            "relearning": self._model_to_dict(
                growth_result.relearning
            ),

            "newlearning": self._model_to_dict(
                growth_result.newlearning
            ),

        }

        confidences = [
            self._normalize_confidence(
                item.get(
                    "confidence",
                    0.0,
                )
            )
            for item in items.values()
            if item
        ]

        for explanation in growth_result.explanations:

            explanation_map = self._model_to_dict(
                explanation
            )

            confidences.append(
                self._normalize_confidence(
                    explanation_map.get(
                        "confidence",
                        0.0,
                    )
                )
            )

        growth_score = (
            sum(confidences)
            /
            len(confidences)
            if confidences
            else 0.0
        )

        return {

            **items,

            "growth_score": round(
                growth_score,
                2,
            ),

            "evidence_count": len(confidences),

        }

    def _build_stable_characteristics(
        self,
        pattern_history: list[dict[str, Any]],
        pattern_average: dict[str, float],
        pattern_trend: dict[str, float],
    ) -> list[dict[str, Any]]:

        if not pattern_history:

            return []

        stable_characteristics = []

        for field in PATTERN_SCORE_FIELDS:

            values = [
                self._to_float(
                    pattern.get(
                        field,
                        0.0,
                    )
                )
                for pattern in pattern_history
            ]

            average = pattern_average.get(
                field,
                0.0,
            )

            trend = pattern_trend.get(
                field,
                0.0,
            )

            spread = (
                max(values)
                -
                min(values)
                if len(values) > 1
                else 0.0
            )

            is_stable = (
                average >= 60
                and abs(trend) <= 15
                and spread <= 30
            )

            if not is_stable:

                continue

            stable_characteristics.append(
                {
                    "metric": field,
                    "average": round(
                        average,
                        2,
                    ),
                    "trend": round(
                        trend,
                        2,
                    ),
                    "spread": round(
                        spread,
                        2,
                    ),
                    "stability_score": round(
                        max(
                            0.0,
                            100.0
                            -
                            spread
                            -
                            abs(trend),
                        ),
                        2,
                    ),
                }
            )

        return sorted(
            stable_characteristics,
            key=lambda item: item[
                "stability_score"
            ],
            reverse=True,
        )

    def _model_to_dict(
        self,
        value,
    ) -> dict[str, Any]:

        if value is None:

            return {}

        if hasattr(
            value,
            "model_dump",
        ):

            return value.model_dump()

        if hasattr(
            value,
            "dict",
        ):

            return value.dict()

        if isinstance(
            value,
            dict,
        ):

            return value

        return {}

    def _normalize_confidence(
        self,
        value,
    ) -> float:

        confidence = self._to_float(
            value
        )

        if 0 <= confidence <= 1:

            return confidence * 100

        return max(
            0.0,
            min(
                confidence,
                100.0,
            ),
        )

    def _to_float(
        self,
        value,
    ) -> float:

        return float(
            value
            or
            0.0
        )
