from app.ai.feature_extractor.constants import (
    CREATIVITY,
    EXECUTION,
    UNCERTAINTY,
)
from app.ai.identity.identity_result import (
    IdentityResult,
)
from app.ai.identity.identity_rules import (
    IDENTITY_RULES,
)


class IdentityEngine:

    """
    Scores every Identity candidate from Layer2 Pattern evidence.
    """

    def analyze(
        self,
        evidence: dict,
    ) -> IdentityResult:

        result = IdentityResult()

        pattern_count = int(
            evidence.get(
                "pattern_count",
                0,
            )
            or
            0
        )

        for warning in evidence.get(
            "warnings",
            [],
        ):

            result.add_warning(
                warning
            )

        if pattern_count <= 0:

            result.set_identity(
                identity_name="Insufficient Pattern Data",
                description=(
                    "Identity requires accumulated Layer2 Pattern data."
                ),
                confidence=0.0,
            )

            result.set_metadata(
                "engine_version",
                "identity_weighted_v2",
            )

            result.set_metadata(
                "source_layer",
                "Layer2 Pattern Data",
            )

            result.set_evidence(
                self._build_result_evidence(
                    evidence=evidence,
                    growth_score=0.0,
                )
            )

            return result

        pattern_scores = evidence.get(
            "pattern_average",
            {},
        )

        trend_scores = evidence.get(
            "pattern_trend",
            {},
        )

        growth_score = self._to_float(
            evidence.get(
                "growth_evidence",
                {},
            ).get(
                "growth_score",
                0.0,
            )
        )

        stable_characteristics = evidence.get(
            "stable_characteristics",
            [],
        )

        candidate_results = []

        for rule in IDENTITY_RULES:

            score, components = self._calculate_score(
                rule=rule,
                pattern_scores=pattern_scores,
                trend_scores=trend_scores,
                growth_score=growth_score,
            )

            stable_matches = self._match_stable_metrics(
                rule=rule,
                stable_characteristics=stable_characteristics,
            )

            candidate_results.append(
                {
                    "rule_id": rule["rule_id"],
                    "identity_key": rule["identity_key"],
                    "identity_name": rule["identity_name"],
                    "description": rule["description"],
                    "score": round(
                        score,
                        2,
                    ),
                    "components": components,
                    "matched_stable_metrics": stable_matches,
                }
            )

        ranking = sorted(
            candidate_results,
            key=lambda candidate: candidate[
                "score"
            ],
            reverse=True,
        )

        primary = ranking[0]

        secondary = (
            ranking[1]
            if len(ranking) > 1
            else None
        )

        score_gap = round(
            primary["score"]
            -
            (
                secondary["score"]
                if secondary
                else 0.0
            ),
            2,
        )

        confidence = self._calculate_confidence(
            primary_score=primary["score"],
            score_gap=score_gap,
            pattern_count=pattern_count,
            stable_characteristics=stable_characteristics,
        )

        result.set_identity(
            identity_name=primary["identity_name"],
            description=primary["description"],
            confidence=confidence,
        )

        result.set_primary_identity(
            primary["identity_name"]
        )

        result.set_secondary_identity(
            secondary["identity_name"]
            if secondary
            else ""
        )

        result.set_score_gap(
            score_gap
        )

        result.set_identity_scores(
            {
                candidate["identity_name"]: candidate[
                    "score"
                ]
                for candidate in ranking
            }
        )

        result.set_ranking(
            [
                {
                    "rank": index,
                    "identity_key": candidate[
                        "identity_key"
                    ],
                    "identity_name": candidate[
                        "identity_name"
                    ],
                    "score": candidate[
                        "score"
                    ],
                    "rule_id": candidate[
                        "rule_id"
                    ],
                }
                for index, candidate in enumerate(
                    ranking,
                    start=1,
                )
            ]
        )

        for candidate in ranking:

            result.add_matched_rule(
                {
                    "rule_id": candidate[
                        "rule_id"
                    ],
                    "identity_name": candidate[
                        "identity_name"
                    ],
                    "score": candidate[
                        "score"
                    ],
                    "components": candidate[
                        "components"
                    ],
                    "matched_stable_metrics": candidate[
                        "matched_stable_metrics"
                    ],
                }
            )

        result.set_scores(
            creativity=int(
                round(
                    self._to_float(
                        pattern_scores.get(
                            CREATIVITY,
                            0,
                        )
                    )
                )
            ),
            execution=int(
                round(
                    self._to_float(
                        pattern_scores.get(
                            EXECUTION,
                            0,
                        )
                    )
                )
            ),
            uncertainty=int(
                round(
                    self._to_float(
                        pattern_scores.get(
                            UNCERTAINTY,
                            0,
                        )
                    )
                )
            ),
        )

        primary_rule = self._get_rule(
            primary["rule_id"]
        )

        for keyword in primary_rule.get(
            "keywords",
            [],
        ):

            result.add_keyword(
                keyword
            )

        for strength in primary_rule.get(
            "strengths",
            [],
        ):

            result.add_strength(
                strength
            )

        for point in primary_rule.get(
            "growth_points",
            [],
        ):

            result.add_growth_point(
                point
            )

        result.set_evidence(
            self._build_result_evidence(
                evidence=evidence,
                growth_score=growth_score,
            )
        )

        result.set_metadata(
            "engine_version",
            "identity_weighted_v2",
        )

        result.set_metadata(
            "source_layer",
            "Layer2 Pattern Data",
        )

        result.set_metadata(
            "candidate_count",
            len(ranking),
        )

        result.set_metadata(
            "pattern_count",
            pattern_count,
        )

        result.set_metadata(
            "primary_rule_id",
            primary["rule_id"],
        )

        return result

    def _calculate_score(
        self,
        rule: dict,
        pattern_scores: dict,
        trend_scores: dict,
        growth_score: float,
    ) -> tuple[float, dict]:

        weights = rule.get(
            "score_weights",
            {},
        )

        pattern_weights = weights.get(
            "pattern",
            {},
        )

        pattern_components = {}

        total_score = 0.0

        for metric, weight in pattern_weights.items():

            metric_score = self._bounded_score(
                pattern_scores.get(
                    metric,
                    0.0,
                )
            )

            contribution = (
                metric_score
                *
                weight
            )

            total_score += contribution

            pattern_components[metric] = {
                "value": metric_score,
                "weight": weight,
                "contribution": round(
                    contribution,
                    2,
                ),
            }

        trend_score = self._calculate_trend_score(
            trend_scores=trend_scores,
            trend_metrics=rule.get(
                "trend_metrics",
                [],
            ),
        )

        trend_weight = self._to_float(
            weights.get(
                "trend",
                0.0,
            )
        )

        trend_contribution = (
            trend_score
            *
            trend_weight
        )

        total_score += trend_contribution

        growth_weight = self._to_float(
            weights.get(
                "growth",
                0.0,
            )
        )

        bounded_growth_score = self._bounded_score(
            growth_score
        )

        growth_contribution = (
            bounded_growth_score
            *
            growth_weight
        )

        total_score += growth_contribution

        return (
            self._bounded_score(
                total_score
            ),
            {
                "pattern": pattern_components,
                "trend": {
                    "metrics": rule.get(
                        "trend_metrics",
                        [],
                    ),
                    "value": trend_score,
                    "weight": trend_weight,
                    "contribution": round(
                        trend_contribution,
                        2,
                    ),
                },
                "growth": {
                    "value": bounded_growth_score,
                    "weight": growth_weight,
                    "contribution": round(
                        growth_contribution,
                        2,
                    ),
                },
            },
        )

    def _calculate_trend_score(
        self,
        trend_scores: dict,
        trend_metrics: list[str],
    ) -> float:

        if not trend_metrics:

            return 50.0

        trend_values = [
            self._to_float(
                trend_scores.get(
                    metric,
                    0.0,
                )
            )
            for metric in trend_metrics
        ]

        average_trend = (
            sum(trend_values)
            /
            len(trend_values)
        )

        return self._bounded_score(
            50.0
            +
            average_trend
        )

    def _match_stable_metrics(
        self,
        rule: dict,
        stable_characteristics: list[dict],
    ) -> list[dict]:

        target_metrics = set(
            rule.get(
                "stable_metrics",
                [],
            )
        )

        return [
            characteristic
            for characteristic in stable_characteristics
            if characteristic.get(
                "metric"
            )
            in target_metrics
        ]

    def _calculate_confidence(
        self,
        primary_score: float,
        score_gap: float,
        pattern_count: int,
        stable_characteristics: list[dict],
    ) -> float:

        score_factor = (
            self._bounded_score(
                primary_score
            )
            /
            100
        )

        data_factor = min(
            pattern_count
            /
            7,
            1.0,
        )

        gap_factor = min(
            max(
                score_gap,
                0.0,
            )
            /
            20,
            1.0,
        )

        stability_factor = min(
            len(stable_characteristics)
            /
            3,
            1.0,
        )

        return round(
            (
                score_factor * 0.45
                +
                data_factor * 0.30
                +
                gap_factor * 0.15
                +
                stability_factor * 0.10
            ),
            2,
        )

    def _build_result_evidence(
        self,
        evidence: dict,
        growth_score: float,
    ) -> dict:

        return {
            "source_layer": "Layer2",
            "pattern_count": evidence.get(
                "pattern_count",
                0,
            ),
            "latest_pattern": evidence.get(
                "latest_pattern",
                {},
            ),
            "pattern_average": evidence.get(
                "pattern_average",
                {},
            ),
            "pattern_trend": evidence.get(
                "pattern_trend",
                {},
            ),
            "stable_characteristics": evidence.get(
                "stable_characteristics",
                [],
            ),
            "feature_scores": evidence.get(
                "feature",
                {},
            ).get(
                "scores",
                {},
            ),
            "growth_evidence": evidence.get(
                "growth_evidence",
                {},
            ),
            "growth_score": round(
                growth_score,
                2,
            ),
        }

    def _get_rule(
        self,
        rule_id: str,
    ) -> dict:

        for rule in IDENTITY_RULES:

            if rule["rule_id"] == rule_id:

                return rule

        return {}

    def _bounded_score(
        self,
        value,
    ) -> float:

        return round(
            max(
                0.0,
                min(
                    self._to_float(
                        value
                    ),
                    100.0,
                ),
            ),
            2,
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
