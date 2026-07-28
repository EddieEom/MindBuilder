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
class NewlearningRule:

    rule_id: str

    feature: str

    min_score: float

    max_score: float

    priority: int

    title: str

    new_belief: str

    action: str

    habit: str

    description: str

    psychology: list[str]


NEWLEARNING_RULES = [

    # =====================================================
    # Future
    # =====================================================

    NewlearningRule(
        rule_id="NL_FUTURE_001",
        feature=FUTURE,
        min_score=70,
        max_score=100,
        priority=100,
        title="예측보다 실행하기",
        new_belief="미래는 예측하는 것이 아니라 경험하며 수정하는 것이다.",
        action="오늘 미래 계획보다 하나의 실행을 시작한다.",
        habit="계획보다 실행 기록을 매일 남긴다.",
        description="미래를 완벽히 계산하기보다 작은 실행을 통해 현실의 데이터를 얻는 연습이 필요합니다.",
        psychology=[
            "Growth Mindset",
            "CBT",
            "Behavior Activation",
        ],
    ),

    # =====================================================
    # Creativity
    # =====================================================

    NewlearningRule(
        rule_id="NL_CREATIVITY_001",
        feature=CREATIVITY,
        min_score=70,
        max_score=100,
        priority=90,
        title="생각보다 선택하기",
        new_belief="좋은 아이디어는 많이 만드는 것이 아니라 끝까지 실행하는 것이다.",
        action="오늘 가장 중요한 아이디어 하나만 선택한다.",
        habit="새로운 아이디어를 시작하기 전에 기존 아이디어 하나를 완료한다.",
        description="창의성은 선택과 집중이 함께할 때 실제 결과로 이어질 수 있습니다.",
        psychology=[
            "Creative Cognition",
            "Decision Making",
        ],
    ),

    # =====================================================
    # Execution
    # =====================================================

    NewlearningRule(
        rule_id="NL_EXECUTION_001",
        feature=EXECUTION,
        min_score=70,
        max_score=100,
        priority=95,
        title="행동으로 검증하기",
        new_belief="생각은 행동을 통해 검증된다.",
        action="5분 안에 시작할 수 있는 첫 행동을 실행한다.",
        habit="새로운 일은 생각보다 먼저 5분 동안 실행해본다.",
        description="완벽한 준비보다 작은 실행이 더 많은 정보를 제공합니다.",
        psychology=[
            "Behavior Activation",
            "Action Bias",
        ],
    ),

    # =====================================================
    # Uncertainty
    # =====================================================

    NewlearningRule(
        rule_id="NL_UNCERTAINTY_001",
        feature=UNCERTAINTY,
        min_score=70,
        max_score=100,
        priority=100,
        title="불확실성과 함께 행동하기",
        new_belief="확실하지 않아도 시작할 수 있다.",
        action="정보가 충분하지 않아도 첫 단계를 실행한다.",
        habit="결정을 미루기보다 제한된 시간 안에 선택하는 연습을 한다.",
        description="불확실성은 제거하는 대상이 아니라 적응하는 대상입니다.",
        psychology=[
            "Acceptance",
            "ACT",
            "CBT",
        ],
    ),

    # =====================================================
    # Perfectionism
    # =====================================================

    NewlearningRule(
        rule_id="NL_PERFECTIONISM_001",
        feature=PERFECTIONISM,
        min_score=70,
        max_score=100,
        priority=95,
        title="완성보다 개선하기",
        new_belief="완벽함보다 반복이 더 큰 성장을 만든다.",
        action="70% 수준에서 결과물을 제출한다.",
        habit="작게 공개하고 피드백을 받는 습관을 만든다.",
        description="실행과 피드백의 반복이 완벽함보다 더 빠른 성장을 만듭니다.",
        psychology=[
            "Growth Mindset",
            "CBT",
        ],
    ),

    # =====================================================
    # Resilience
    # =====================================================

    NewlearningRule(
        rule_id="NL_RESILIENCE_001",
        feature=RESILIENCE,
        min_score=0,
        max_score=35,
        priority=90,
        title="회복을 일정에 포함하기",
        new_belief="회복은 성장을 위한 투자이다.",
        action="오늘 20분의 회복 시간을 일정에 등록한다.",
        habit="매주 회복 시간을 가장 먼저 일정에 추가한다.",
        description="지속 가능한 성장은 회복을 포함한 리듬에서 만들어집니다.",
        psychology=[
            "Recovery Theory",
            "Self Regulation",
        ],
    ),

    # =====================================================
    # Overload
    # =====================================================

    NewlearningRule(
        rule_id="NL_OVERLOAD_001",
        feature=OVERLOAD,
        min_score=60,
        max_score=100,
        priority=100,
        title="인지 자원 보호하기",
        new_belief="많이 하는 것이 아니라 중요한 것을 끝내는 것이 성장이다.",
        action="오늘 반드시 끝낼 일 하나만 선택한다.",
        habit="하루 목표를 최대 3개 이하로 유지한다.",
        description="인지 자원을 분산시키기보다 가장 중요한 일에 집중하는 연습이 필요합니다.",
        psychology=[
            "Cognitive Load Theory",
            "Executive Function",
        ],
    ),

]