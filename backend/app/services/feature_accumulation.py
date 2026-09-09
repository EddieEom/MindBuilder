from copy import deepcopy

from app.ai.feature_extractor.feature_result import FeatureResult


def accumulate_features(observation: FeatureResult, previous: dict) -> FeatureResult:
    """Carry missing features without manufacturing new observations or confidence."""
    state = deepcopy(observation)
    carried = {}
    for code, row in previous.items():
        if observation.get_confidence(code) > 0:
            continue
        state.scores[code] = float(row.feature_value)
        state.confidence[code] = float(row.confidence_score)
        carried[code] = row.scan_id
    state.metadata["carried_features"] = carried
    state.metadata["observed_features"] = [
        code for code in observation.scores if observation.get_confidence(code) > 0
    ]
    state.metadata["accumulation_version"] = "latest_observation_v1"
    return state
