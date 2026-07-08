# Feature Names

FUTURE = "future_score"
EXECUTION = "execution_score"
CREATIVITY = "creativity_score"
UNCERTAINTY = "uncertainty_score"
PERFECTIONISM = "perfectionism_score"
RESILIENCE = "resilience_score"
OVERLOAD = "overload_score"
THINKING_PATTERN = "thinking_pattern"
SELF_EVALUATION = "self_evaluation"
STRESS_PATTERN = "stress_pattern"
CBT = "CBT"
EXECUTIVE_FUNCTION = "Executive Function"
SDT = "Self Determination Theory"
BANDURA = "Bandura"
DWECK = "Dweck"
KAHNEMAN = "Kahneman"

FEATURE_KEYS = [
    FUTURE,
    EXECUTION,
    CREATIVITY,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
    OVERLOAD,
]

TOP_PATTERN_COUNT = 3

# =========================
# Rule Weight
# =========================

NONE = 0

WEAK = 1
MEDIUM = 2
STRONG = 3


WEIGHT_SCORE = {
    NONE: 0,
    WEAK: 5,
    MEDIUM: 15,
    STRONG: 25,
}


# Gap Severity
GAP_LOW = 1
GAP_MEDIUM = 2
GAP_HIGH = 3

GAP_SCORE = {
    GAP_LOW: 10,
    GAP_MEDIUM: 20,
    GAP_HIGH: 30,
}
