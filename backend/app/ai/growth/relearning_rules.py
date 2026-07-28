from dataclasses import dataclass

from app.ai.feature_extractor.constants import (
    FUTURE,
    CREATIVITY,
    EXECUTION,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
    OVERLOAD,
)


@dataclass(frozen=True)
class RelearningRule:

    rule_id: str

    feature: str

    min_score: float

    max_score: float

    priority: int

    title: str

    root_cause: str

    mechanism: str

    description: str

    psychology: list[str]


RELEARNING_RULES = [

    # =====================================================
    # Future
    # =====================================================

    RelearningRule(
        rule_id="RL_FUTURE_001",
        feature=FUTURE,
        min_score=70,
        max_score=100,
        priority=100,
        title="미래가 문제가 아니라 미래를 통제하려고 하고 있습니다.",
        root_cause="불확실성을 줄이기 위해 미래를 반복적으로 시뮬레이션하고 있습니다.",
        mechanism="불안 → 미래 예측 → 일시적 안심 → 다시 불안",
        description="미래를 준비하는 능력은 강점입니다. 하지만 미래를 계속 예측해야만 안심되는 상태라면 사고 에너지가 현재보다 미래에 과도하게 사용됩니다.",
        psychology=[
            "Intolerance of Uncertainty",
            "CBT",
            "Executive Function",
        ],
    ),

    # =====================================================
    # Creativity
    # =====================================================

    RelearningRule(
        rule_id="RL_CREATIVITY_001",
        feature=CREATIVITY,
        min_score=70,
        max_score=100,
        priority=95,
        title="아이디어가 부족한 것이 아니라 선택 기준이 부족합니다.",
        root_cause="여러 가능성을 동시에 유지하려는 경향이 있습니다.",
        mechanism="아이디어 생성 → 새로운 가능성 발견 → 선택 보류",
        description="창의성은 높지만 무엇을 버릴지를 결정하는 기준이 부족하면 실행보다 탐색이 길어질 수 있습니다.",
        psychology=[
            "Divergent Thinking",
            "Creative Cognition",
        ],
    ),

    # =====================================================
    # Execution
    # =====================================================

    RelearningRule(
        rule_id="RL_EXECUTION_001",
        feature=EXECUTION,
        min_score=70,
        max_score=100,
        priority=90,
        title="실행력이 부족한 것이 아니라 생각이 행동보다 앞서고 있습니다.",
        root_cause="행동 전에 충분히 검증해야 한다는 사고가 있습니다.",
        mechanism="생각 → 검증 → 재검증 → 실행 지연",
        description="행동 능력이 부족한 것이 아니라 사고 과정이 길어져 실행이 늦어질 가능성이 있습니다.",
        psychology=[
            "Analysis Paralysis",
            "Executive Function",
        ],
    ),

    # =====================================================
    # Uncertainty
    # =====================================================

    RelearningRule(
        rule_id="RL_UNCERTAINTY_001",
        feature=UNCERTAINTY,
        min_score=70,
        max_score=100,
        priority=100,
        title="불확실성이 문제가 아니라 불확실성을 위험으로 해석하고 있습니다.",
        root_cause="예측할 수 없는 상황을 위험 신호로 인식하는 경향이 있습니다.",
        mechanism="불확실성 → 위험 인식 → 불안 증가 → 통제 시도",
        description="실제 위험보다 예상되는 위험에 더 많은 인지 자원을 사용할 가능성이 있습니다.",
        psychology=[
            "Intolerance of Uncertainty",
            "CBT",
        ],
    ),

    # =====================================================
    # Perfectionism
    # =====================================================

    RelearningRule(
        rule_id="RL_PERFECTIONISM_001",
        feature=PERFECTIONISM,
        min_score=70,
        max_score=100,
        priority=95,
        title="완벽주의가 문제가 아니라 실수를 위협으로 해석하고 있습니다.",
        root_cause="실수 자체보다 실수의 결과를 크게 예상하는 경향이 있습니다.",
        mechanism="실수 예상 → 불안 → 시작 지연",
        description="높은 기준은 장점이지만 행동을 막는 기준이 되면 성장보다 회피가 강화될 수 있습니다.",
        psychology=[
            "CBT",
            "Self Criticism",
        ],
    ),

    # =====================================================
    # Resilience
    # =====================================================

    RelearningRule(
        rule_id="RL_RESILIENCE_001",
        feature=RESILIENCE,
        min_score=0,
        max_score=35,
        priority=90,
        title="회복 능력이 부족한 것이 아니라 회복을 허용하지 않고 있습니다.",
        root_cause="쉬는 시간을 생산성이 없는 시간으로 인식하는 경향이 있습니다.",
        mechanism="피로 → 휴식 미룸 → 에너지 감소 → 생산성 저하",
        description="회복은 낭비가 아니라 다음 행동을 위한 투자입니다.",
        psychology=[
            "Recovery Theory",
            "Self Regulation",
        ],
    ),

    # =====================================================
    # Overload
    # =====================================================

    RelearningRule(
        rule_id="RL_OVERLOAD_001",
        feature=OVERLOAD,
        min_score=60,
        max_score=100,
        priority=100,
        title="해야 할 일이 많은 것이 아니라 인지 자원이 과도하게 사용되고 있습니다.",
        root_cause="여러 문제를 동시에 해결하려고 하면서 작업 기억이 지속적으로 사용되고 있습니다.",
        mechanism="과제 증가 → 인지 부하 → 결정 피로 → 실행 감소",
        description="시간이 부족한 것이 아니라 뇌가 동시에 처리하는 정보량이 많아지고 있습니다.",
        psychology=[
            "Cognitive Load Theory",
            "Executive Function",
        ],
    ),
]