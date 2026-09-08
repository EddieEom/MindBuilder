from types import SimpleNamespace

import pytest

from app.ai.feature_extractor.feature_extractor import FeatureExtractor
from app.ai.feature_extractor.feature_result import FeatureResult
from app.ai.feature_extractor.rule_policy import RULESET_VERSION, RuleQualityPolicy


def test_same_question_evidence_is_deduplicated_before_combining():
    result = FeatureResult()
    result.add_confidence("future_score", .60, "QUESTION:2:future_score")
    result.add_confidence("future_score", .50, "QUESTION:2:future_score")
    assert result.get_confidence("future_score") == pytest.approx(.60)

    result.add_confidence("future_score", .50, "QUESTION:6:future_score")
    assert result.get_confidence("future_score") == pytest.approx(.80)


def test_self_report_and_pattern_priors_are_calibrated():
    option = RuleQualityPolicy.option(2, "future_score", .95)
    assert option.raw_confidence == .95
    assert option.confidence <= .65
    assert option.evidence_group == "QUESTION:2:future_score"
    assert RuleQualityPolicy.pattern(.95, 2) <= .80


def test_extractor_persists_auditable_rule_metadata():
    answer = SimpleNamespace(question_id=2, option_id=10)
    result = FeatureExtractor().extract_features([answer])
    evidence = result.evidences["future_score"][0]
    assert evidence["raw_confidence"] == .95
    assert evidence["confidence"] < evidence["raw_confidence"]
    assert evidence["source_type"] == "SELF_REPORT"
    assert evidence["rule_version"] == RULESET_VERSION
    assert evidence["evidence_group"] == "QUESTION:2:future_score"
