from dataclasses import dataclass
from typing import List

# 추후에 core_belief, thinking_pattern은 따로 분리해서 관리할 수 있도록 개선 필요
# ==========================================================
# Unlearning Rule
# ==========================================================

@dataclass(frozen=True)
class UnlearningRule:

    rule_id: str

    feature: str

    min_score: float

    max_score: float

    priority: int

    thinking_pattern: str

    core_belief: str

    title: str

    description: str


# ==========================================================
# Seed Rules
# ==========================================================

UNLEARNING_RULES: List[UnlearningRule] = [

    # ======================================================
    # Future
    # ======================================================

    UnlearningRule(

        rule_id="UNL_FUTURE_01",

        feature="future_score",

        min_score=70,

        max_score=100,

        priority=1,

        thinking_pattern="Future Simulation",

        core_belief="미래를 예측해야만 안전하다.",

        title="미래를 모두 예측해야 한다.",

        description=(
            "미래를 완벽히 예측하려는 사고가 현재의 행동보다 "
            "시뮬레이션에 에너지를 소비하게 만들고 있습니다."
        ),
    ),

    UnlearningRule(

        rule_id="UNL_FUTURE_02",

        feature="future_score",

        min_score=50,

        max_score=69,

        priority=2,

        thinking_pattern="Future Concern",

        core_belief="계획이 완벽해야 시작할 수 있다.",

        title="완벽한 계획이 있어야 시작할 수 있다.",

        description=(
            "계획 자체보다 실행을 통해 정보를 얻는 과정이 "
            "더 중요한 시점일 수 있습니다."
        ),
    ),

    # ======================================================
    # Overload
    # ======================================================

    UnlearningRule(

        rule_id="UNL_OVERLOAD_01",

        feature="overload_score",

        min_score=70,

        max_score=100,

        priority=1,

        thinking_pattern="Cognitive Overload",

        core_belief="멈추면 뒤처진다.",

        title="쉬면 뒤처진다.",

        description=(
            "휴식을 손실로 인식하여 인지 자원을 지속적으로 "
            "소모하고 있습니다."
        ),
    ),

    UnlearningRule(

        rule_id="UNL_OVERLOAD_02",

        feature="overload_score",

        min_score=50,

        max_score=69,

        priority=2,

        thinking_pattern="Responsibility Bias",

        core_belief="모든 책임은 내가 해결해야 한다.",

        title="모든 문제를 내가 해결해야 한다.",

        description=(
            "책임감을 지나치게 개인화하면서 인지 부하가 "
            "증가하고 있습니다."
        ),
    ),

    # ======================================================
    # Perfectionism
    # ======================================================

    UnlearningRule(

        rule_id="UNL_PERFECTION_01",

        feature="perfectionism_score",

        min_score=70,

        max_score=100,

        priority=1,

        thinking_pattern="Error Avoidance",

        core_belief="완벽해야 인정받는다.",

        title="완벽해야 가치가 있다.",

        description=(
            "실수를 성장 과정이 아닌 실패로 해석하는 "
            "사고가 나타나고 있습니다."
        ),
    ),

    # ======================================================
    # Uncertainty
    # ======================================================

    UnlearningRule(

        rule_id="UNL_UNCERTAINTY_01",

        feature="uncertainty_score",

        min_score=70,

        max_score=100,

        priority=1,

        thinking_pattern="Threat Prediction",

        core_belief="불확실성은 위험하다.",

        title="불확실성은 피해야 한다.",

        description=(
            "예측 불가능성을 위험으로 해석하는 경향이 "
            "높게 나타나고 있습니다."
        ),
    ),

    # ======================================================
    # Execution
    # ======================================================

    UnlearningRule(

        rule_id="UNL_EXECUTION_01",

        feature="execution_score",

        min_score=80,

        max_score=100,

        priority=3,

        thinking_pattern="Achievement Dependence",

        core_belief="성과가 나의 가치다.",

        title="성과가 나의 가치다.",

        description=(
            "성과 중심 사고가 자기 가치와 강하게 "
            "연결되어 있습니다."
        ),
    ),

    # ======================================================
    # Creativity
    # ======================================================

    UnlearningRule(

        rule_id="UNL_CREATIVITY_01",

        feature="creativity_score",

        min_score=80,

        max_score=100,

        priority=3,

        thinking_pattern="Idea Attachment",

        core_belief="좋은 아이디어를 모두 실행해야 한다.",

        title="모든 아이디어를 놓치면 안 된다.",

        description=(
            "아이디어 생성보다 선택과 집중이 "
            "필요한 시점일 수 있습니다."
        ),
    ),

    # ======================================================
    # Resilience
    # ======================================================

    UnlearningRule(

        rule_id="UNL_RESILIENCE_01",

        feature="resilience_score",

        min_score=0,

        max_score=30,

        priority=2,

        thinking_pattern="Low Recovery",

        core_belief="회복은 사치다.",

        title="회복보다 버티는 것이 중요하다.",

        description=(
            "회복을 미루는 사고가 장기적으로 "
            "성장을 방해할 가능성이 있습니다."
        ),
    ),
]