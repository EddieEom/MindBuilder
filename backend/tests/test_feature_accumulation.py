from types import SimpleNamespace

from app.ai.feature_extractor.feature_result import FeatureResult
from app.services.feature_accumulation import accumulate_features


def test_missing_feature_preserves_last_observation_without_new_evidence():
    raw = FeatureResult(scores={"execution_score": 0}, confidence={})
    previous = {"execution_score": SimpleNamespace(feature_value=72, confidence_score=.6, scan_id=1)}
    state = accumulate_features(raw, previous)
    assert state.get_score("execution_score") == 72
    assert state.get_confidence("execution_score") == .6
    assert not state.evidences
    assert raw.get_score("execution_score") == 0
    assert state.metadata["carried_features"] == {"execution_score": 1}


def test_observed_zero_replaces_previous_score():
    raw = FeatureResult(scores={"execution_score": 0}, confidence={"execution_score": .5})
    previous = {"execution_score": SimpleNamespace(feature_value=72, confidence_score=.6, scan_id=1)}
    state = accumulate_features(raw, previous)
    assert state.get_score("execution_score") == 0
    assert state.metadata["carried_features"] == {}
