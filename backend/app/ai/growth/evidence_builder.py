from __future__ import annotations

from statistics import mean
from typing import Any


class EvidenceBuilder:
    """
    FeatureResult
        ↓
    EvidenceBuilder
        ↓
    EvidenceMap

    GrowthEngine와 PromptBuilder가 사용할
    표준 Evidence 구조를 생성한다.
    """

    def build(
        self,
        feature_result,
    ) -> dict[str, dict]:

        evidence_map = {}

        for feature_name, score in feature_result.scores.items():

            evidence_map[feature_name] = self._build_feature(
                feature_name=feature_name,
                feature_result=feature_result,
            )

        return evidence_map

    # =======================================================
    # Private
    # =======================================================

    def _build_feature(
        self,
        feature_name: str,
        feature_result,
    ) -> dict:

        evidences = feature_result.evidences.get(
            feature_name,
            [],
        )

        evidences = self._sort_evidences(
            evidences,
        )

        return {

            "feature": feature_name,

            "score": feature_result.scores.get(
                feature_name,
                0.0,
            ),

            "confidence": feature_result.confidences.get(
                feature_name,
                0.0,
            ),

            "strength": self._calculate_strength(
                evidences,
            ),

            "evidence_count": len(
                evidences,
            ),

            "top_evidence": (
                evidences[0]
                if evidences
                else None
            ),

            "evidences": evidences,

        }

    # =======================================================
    # Evidence Sort
    # =======================================================

    def _sort_evidences(
        self,
        evidences: list[dict],
    ) -> list[dict]:

        return sorted(

            evidences,

            key=lambda e: (

                e.get("confidence", 0),

                e.get("weight", 0),

            ),

            reverse=True,

        )

    # =======================================================
    # Evidence Strength
    # =======================================================

    def _calculate_strength(
        self,
        evidences: list[dict],
    ) -> float:

        if not evidences:
            return 0.0

        values = []

        for evidence in evidences:

            confidence = evidence.get(
                "confidence",
                0.0,
            )

            weight = evidence.get(
                "weight",
                1.0,
            )

            values.append(
                confidence * weight
            )

        strength = mean(values)

        return round(
            min(
                strength,
                1.0,
            ),
            3,
        )