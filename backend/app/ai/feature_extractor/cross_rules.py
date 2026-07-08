# 질문간 관계

"""
==========================================================
MindBuilder Rule Engine

Cross Rules

Feature Extraction 이후
질문 간 관계를 분석하는 규칙

1. Reinforcement Rule
2. Conflict Rule
3. Confidence Rule
4. Interpretation Rule
==========================================================
"""

from app.ai.feature_extractor.constants import (
    FUTURE,
    EXECUTION,
    CREATIVITY,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
    OVERLOAD,
    GAP_LOW,
    GAP_MEDIUM,
    GAP_HIGH,
    CBT,
    KAHNEMAN,
    EXECUTIVE_FUNCTION,
    BANDURA,
    DWECK
    
)

# ==========================================================
# Reinforcement Rule
#
# 같은 Feature가 여러 질문에서 반복되면
# 해당 Feature의 신뢰도를 증가시킨다.
# ==========================================================

REINFORCEMENT_RULES = [

    # ======================================================
    # FUTURE
    # ======================================================

    {
        "rule_id": "RF_FUTURE_01",

        "conditions": [
            10,     # Q2 미래
            44,     # Q6 미래
        ],

        "feature": FUTURE,

        "bonus": 2,


        "reason": "미래에 대한 사고가 고민과 긴장에서 반복적으로 나타난다.",
    },

    {
        "rule_id": "RF_FUTURE_02",

        "conditions": [
            10,
            49,
        ],

        "feature": FUTURE,

        "bonus": 1,

        "reason": "미래지향적 사고가 학업 영역에서도 나타난다.",
    },

    {
        "rule_id": "RF_FUTURE_03",

        "conditions": [
            43,     # 커리어
            44,     # 미래
        ],

        "feature": FUTURE,

        "bonus": 1,

        "reason": "커리어와 미래가 동일한 미래지향적 사고축으로 연결된다.",
    },


    {
        "rule_id": "RF_FUTURE_04",

        "conditions": [
            44,
            21,
        ],

        "feature": FUTURE,

        "bonus": 1,

        "reason": "미래에 대한 불안이 행동 저해와 연결된다.",
    },

    {
        "rule_id": "RF_FUTURE_05",

        "conditions": [
            10,
            43,
            44,
        ],

        "feature": FUTURE,

        "bonus": 4,

        "reason": "미래 사고가 커리어와 미래 긴장으로 일관되게 나타난다.",
    },

    {
        "rule_id": "RF_FUTURE_06",

        "conditions": [
            10,
            44,
            49,
        ],

        "feature": FUTURE,

        "bonus": 3,

        "reason": "미래 사고가 학업과 미래 긴장으로 연결된다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_07",

        "conditions": [
            11,
            21,
            44,
        ],

        "feature": UNCERTAINTY,

        "bonus": 5,

        "reason": "자기 의심, 불안, 미래 긴장이 동시에 나타난다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_08",

        "conditions": [
            12,
            11,
            21,
        ],

        "feature": UNCERTAINTY,

        "bonus": 4,

        "reason": "타인 비교와 자기 의심이 불안으로 이어지고 있다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_09",

        "conditions": [
            10,
            21,
            44,
        ],

        "feature": UNCERTAINTY,

        "bonus": 4,

        "reason": "미래 중심 사고가 미래 불안으로 강화되고 있다.",
    },

    # ======================================================
    # EXECUTION
    # ======================================================

    {
        "rule_id": "RF_EXECUTION_01",

        "conditions": [
            8,
            18,
        ],

        "feature": EXECUTION,

        "bonus": 3,

        "reason": "우선순위 결정 문제로 실행이 반복적으로 지연된다.",
    },

    {
        "rule_id": "RF_EXECUTION_02",

        "conditions": [
            8,
            24,
        ],

        "feature": EXECUTION,

        "bonus": 2,

        "reason": "방향성 부족과 계획 부족이 동시에 나타난다.",
    },

    {
        "rule_id": "RF_EXECUTION_03",

        "conditions": [
            22,
            23,
        ],

        "feature": EXECUTION,

        "bonus": 1,

        "reason": "완벽주의와 집중 저하가 실행력을 동시에 방해한다.",
    },

    {
        "rule_id": "RF_EXECUTION_04",

        "conditions": [
            18,
            23,
        ],

        "feature": EXECUTION,

        "bonus": 2,

        "reason": "우선순위 문제와 집중 저하가 동시에 실행력을 저하시킨다.",
    },

    {
        "rule_id": "RF_EXECUTION_05",

        "conditions": [
            24,
            23,
        ],

        "feature": EXECUTION,

        "bonus": 2,

        "reason": "계획 부족과 집중 저하가 함께 나타난다.",
    },

    {
        "rule_id": "RF_EXECUTION_06",

        "conditions": [
            17,
            18,
        ],

        "feature": EXECUTION,

        "bonus": 2,

        "reason": "과도한 사고와 방향 혼란이 동시에 행동을 지연시킨다.",
    },

    {
        "rule_id": "RF_EXECUTION_07",

        "conditions": [
            8,     # 방향을 모르겠다
            18,    # 무엇부터 해야할지 모르겠다
            24,    # 계획이 없다
        ],

        "feature": EXECUTION,

        "bonus": 4,

        "reason": "방향성 부족, 우선순위 혼란, 계획 부족이 동시에 확인된다.",
    },

    {
        "rule_id": "RF_EXECUTION_08",

        "conditions": [
            17,
            18,
            23,
        ],

        "feature": EXECUTION,

        "bonus": 3,

        "reason": "과도한 사고와 우선순위 혼란이 집중 저하로 이어지고 있다.",
    },

    # ======================================================
    # OVERLOAD
    # ======================================================

    {
        "rule_id": "RF_OVERLOAD_01",

        "conditions": [
            9,
            19,
        ],

        "feature": OVERLOAD,

        "bonus": 2,

        "reason": "업무 과부하와 시간 부족이 함께 나타난다.",
    },

    {
        "rule_id": "RF_OVERLOAD_02",

        "conditions": [
            9,
            20,
        ],

        "feature": OVERLOAD,

        "bonus": 3,

        "reason": "과도한 업무량으로 에너지 고갈이 발생하고 있다.",
    },

    {
        "rule_id": "RF_OVERLOAD_03",

        "conditions": [
            13,
            20,
        ],

        "feature": OVERLOAD,

        "bonus": 3,

        "reason": "회복 부족과 에너지 부족이 동시에 확인된다.",
    },

    {
        "rule_id": "RF_OVERLOAD_04",

        "conditions": [
            13,
            46,
        ],

        "feature": OVERLOAD,

        "bonus": 2,

        "reason": "프로젝트 수행으로 회복 부족이 심화되고 있다.",
    },


    {
        "rule_id": "RF_OVERLOAD_05",

        "conditions": [
            20,
            46,
        ],

        "feature": OVERLOAD,

        "bonus": 2,

        "reason": "에너지 부족과 프로젝트 부담이 동일한 과부하 상태를 만든다.",
    },

    {
        "rule_id": "RF_OVERLOAD_06",

        "conditions": [
            19,
            46,
        ],

        "feature": OVERLOAD,

        "bonus": 2,

        "reason": "시간 부족과 프로젝트 부담이 함께 나타난다.",
    },

    {
        "rule_id": "RF_OVERLOAD_07",

        "conditions": [
            9,
            13,
        ],

        "feature": OVERLOAD,

        "bonus": 2,

        "reason": "업무 과부하가 회복 부족으로 이어지고 있다.",
    },

    {
        "rule_id": "RF_OVERLOAD_08",

        "conditions": [
            9,
            19,
            46,
        ],

        "feature": OVERLOAD,

        "bonus": 4,

        "reason": "업무량, 시간 부족, 프로젝트 부담이 동시에 나타난다.",
    },

    {
        "rule_id": "RF_OVERLOAD_09",

        "conditions": [
            9,
            20,
            13,
        ],

        "feature": OVERLOAD,

        "bonus": 5,

        "reason": "과부하가 에너지 고갈과 회복 부족으로 이어지고 있다.",
    },

    {
        "rule_id": "RF_OVERLOAD_10",

        "conditions": [
            13,
            20,
            46,
        ],

        "feature": OVERLOAD,

        "bonus": 4,

        "reason": "프로젝트 부담으로 회복 부족과 피로가 지속되고 있다.",
    },
    # ======================================================
    # UNCERTAINTY
    # ======================================================

    {
        "rule_id": "RF_UNCERTAINTY_01",

        "conditions": [
            11,
            21,
        ],

        "feature": UNCERTAINTY,

        "bonus": 3,

        "reason": "자기 의심과 불안이 동시에 나타난다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_02",

        "conditions": [
            10,
            44,
        ],

        "feature": UNCERTAINTY,

        "bonus": 2,

        "reason": "미래 사고와 미래 긴장이 함께 나타난다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_03",

        "conditions": [
            12,
            11,
        ],

        "feature": UNCERTAINTY,

        "bonus": 2,

        "reason": "타인 비교와 자기 의심이 함께 나타난다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_04",

        "conditions": [
            21,
            44,
        ],

        "feature": UNCERTAINTY,

        "bonus": 2,

        "reason": "불안과 미래 긴장이 동일한 불확실성 기반으로 나타난다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_05",

        "conditions": [
            10,
            21,
        ],

        "feature": UNCERTAINTY,

        "bonus": 2,


        "reason": "미래 중심 사고가 불안으로 연결되고 있다.",
    },

    {
        "rule_id": "RF_UNCERTAINTY_06",

        "conditions": [
            18,
            11,
        ],

        "feature": UNCERTAINTY,

        "bonus": 1,

        "reason": "방향 혼란과 자기 의심이 동시에 나타난다.",
    },

    # ======================================================
    # PERFECTIONISM
    # ======================================================

    {
        "rule_id": "RF_PERFECTIONISM_01",

        "conditions": [
            11,
            22,
        ],

        "feature": PERFECTIONISM,

        "bonus": 2,


        "reason": "자기 검증과 완벽주의가 함께 나타난다.",
    },

    {
        "rule_id": "RF_PERFECTIONISM_02",

        "conditions": [
            12,
            22,
        ],

        "feature": PERFECTIONISM,

        "bonus": 2,

        "reason": "타인 비교와 완벽주의가 함께 나타난다.",
    },

    {
        "rule_id": "RF_PERFECTIONISM_03",

        "conditions": [
            22,
            17,
        ],

        "feature": PERFECTIONISM,

        "bonus": 1,

        "reason": "과도한 사고가 완벽주의와 함께 나타난다.",
    },

    {
        "rule_id": "RF_PERFECTIONISM_04",

        "conditions": [
            11,
            22,
            17,
        ],

        "feature": PERFECTIONISM,

        "bonus": 3,

        "reason": "자기 검증과 완벽주의가 과도한 사고를 유발하고 있다.",
    },

    {
        "rule_id": "RF_PERFECTIONISM_05",

        "conditions": [
            12,
            22,
            21,
        ],

        "feature": PERFECTIONISM,

        "bonus": 4,

        "reason": "타인 비교와 완벽주의가 불안을 강화하고 있다.",
    },

    # ======================================================
    # RESILIENCE
    # ======================================================

    {
        "rule_id": "RF_RESILIENCE_01",

        "conditions": [
            13,
            48,
        ],

        "feature": RESILIENCE,

        "bonus": -2,

        "reason": "회복 부족과 건강 문제가 동시에 나타난다.",
    },

    {
        "rule_id": "RF_RESILIENCE_02",

        "conditions": [
            20,
            48,
        ],

        "feature": RESILIENCE,

        "bonus": -2,

        "reason": "에너지 부족과 건강 우려가 함께 나타난다.",
    },

    {
        "rule_id": "RF_RESILIENCE_03",

        "conditions": [
            13,
            20,
            48,
        ],

        "feature": RESILIENCE,

        "bonus": -3,

        "reason": "회복 부족, 에너지 저하, 건강 우려가 동시에 나타난다.",
    },

    {
        "rule_id": "RF_RESILIENCE_04",

        "conditions": [
            20,
            47,
        ],

        "feature": RESILIENCE,

        "bonus": -1,

        "reason": "에너지 부족과 대인관계 소모가 함께 나타난다.",
    },


    {
        "rule_id": "RF_RESILIENCE_05",

        "conditions": [
            13,
            20,
            47,
        ],

        "feature": RESILIENCE,

        "bonus": -3,


        "reason": "회복 부족과 피로가 대인관계 스트레스로 이어지고 있다.",
    },

    {
        "rule_id": "RF_RESILIENCE_06",

        "conditions": [
            13,
            20,
            48,
        ],

        "feature": RESILIENCE,

        "bonus": -4,

        "reason": "회복 부족과 피로가 건강 우려까지 확장되고 있다.",
    },

    # ======================================================
    # CREATIVITY
    # ======================================================

     {
        "rule_id": "RF_CREATIVITY_01",

        "conditions": [
            14,
            38,
        ],

        "feature": CREATIVITY,

        "bonus": 3,


        "reason": "창의적 사고가 실제 창작 행동으로 이어지고 있다.",
    },

    {
        "rule_id": "RF_CREATIVITY_02",

        "conditions": [
            14,     # 아이디어
            38,     # 창작
            30,     # 성장감
        ],

        "feature": CREATIVITY,

        "bonus": 4,


        "reason": "창의적 사고가 실제 창작 행동과 성장 욕구로 이어지고 있다.",
    },

    {
        "rule_id": "RF_CREATIVITY_03",

        "conditions": [
            14,
            38,
            43,
        ],

        "feature": CREATIVITY,

        "bonus": 3,


        "reason": "창의적 사고가 실제 행동으로 이어지며 커리어 관심과 연결된다.",
    },
]







# ==================================================================================================

CONFLICT_RULES = [

    # ======================================================
    # EXECUTION
    # ======================================================
    {
        "rule_id": "CF_EXECUTION_01",

        "current": [8],

        "target": 27,

        "gap": EXECUTION,

        "severity": GAP_HIGH,

        "reason": "현재 방향성을 잃었지만 명확한 방향을 원하고 있다.",
    },

    {
        "rule_id": "CF_EXECUTION_02",

        "current": [24],

        "target": 27,

        "gap": EXECUTION,

        "severity": GAP_HIGH,

        "reason": "계획 부족으로 인해 방향성에 대한 요구가 커지고 있다.",
    },
  
    {
        "rule_id": "CF_EXECUTION_03",

        "current": [18],

        "target": 27,

        "gap": EXECUTION,

        "severity": GAP_HIGH,

        "reason": "우선순위 혼란으로 인해 명확한 방향을 원하고 있다.",
    },

    {
        "rule_id": "CF_EXECUTION_04",

        "current": [
            44,     # 미래
        ],

        "target": 27,      # 명확한 방향

        "gap": EXECUTION,

        "severity": GAP_MEDIUM,

        "reason": "미래에 대한 긴장이 현재 행동 방향의 명확성을 요구하고 있다.",
    },

    # ======================================================
    # RESILIENCE
    # ======================================================

    {
        "rule_id": "CF_RESILIENCE_01",

        "current": [13],

        "target": 31,

        "gap": RESILIENCE,

        "severity": GAP_HIGH,

        "reason": "회복이 부족한 상태에서 휴식을 가장 필요로 하고 있다.",
    },

    {
        "rule_id": "CF_RESILIENCE_02",

        "current": [20],

        "target": 31,

        "gap": RESILIENCE,

        "severity": GAP_HIGH,

        "reason": "지속적인 피로로 인해 회복 욕구가 커지고 있다.",
    },

    {
        "rule_id": "CF_RESILIENCE_03",

        "current": [48],

        "target": 31,

        "gap": RESILIENCE,

        "severity": GAP_MEDIUM,

        "reason": "건강에 대한 긴장이 휴식 욕구로 이어지고 있다.",
    },

    {
        "rule_id": "CF_RESILIENCE_04",

        "current": [
            13,
            20,
        ],

        "target": 31,

        "gap": RESILIENCE,

        "severity": GAP_HIGH,

        "reason": "회복 부족과 에너지 저하가 동시에 나타나며 휴식을 가장 필요로 하고 있다.",
    },

    {
        "rule_id": "CF_RESILIENCE_05",

        "current": [
            46,     # 프로젝트
        ],

        "target": 31,      # 휴식

        "gap": RESILIENCE,

        "severity": GAP_MEDIUM,

        "reason": "프로젝트 수행으로 인한 긴장이 회복과 휴식의 필요성으로 이어지고 있다.",
    },

    # ======================================================
    # UNCERTAINTY
    # ======================================================

    {
        "rule_id": "CF_UNCERTAINTY_01",

        "current": [11],

        "target": 33,

        "gap": UNCERTAINTY,

        "severity": GAP_HIGH,

        "reason": "자기 확신 부족으로 인해 자신감을 가장 원하고 있다.",
    },

    {
        "rule_id": "CF_UNCERTAINTY_02",

        "current": [21],

        "target": 33,

        "gap": UNCERTAINTY,

        "severity": GAP_HIGH,

        "reason": "불안이 자신감 부족으로 이어지고 있다.",
    },

    {
        "rule_id": "CF_UNCERTAINTY_03",

        "current": [12],

        "target": 33,

        "gap": UNCERTAINTY,

        "severity": GAP_MEDIUM,

        "reason": "타인 비교로 인해 자기 확신을 잃고 있다.",
    },

    {
        "rule_id": "CF_UNCERTAINTY_04",

        "current": [
            11,     # 잘하고 있는지 의심
            21,     # 불안하다
        ],

        "target": 33,      # 자신감

        "gap": UNCERTAINTY,

        "severity": GAP_HIGH,

        "reason": "자기 의심과 불안이 동시에 나타나며 자신감을 가장 필요로 하고 있다.",
    },


    # ======================================================
    # FUTURE
    # ======================================================

    {
        "rule_id": "CF_FUTURE_01",

        "current": [10],

        "target": 30,

        "gap": FUTURE,

        "severity": GAP_MEDIUM,

        "reason": "미래에 대한 고민을 성장으로 전환하고 싶어 한다.",
    },

    {
        "rule_id": "CF_FUTURE_02",

        "current": [43],

        "target": 30,

        "gap": FUTURE,

        "severity": GAP_MEDIUM,

        "reason": "커리어 고민을 성장의 기회로 만들고 싶어 한다.",
    },

    {
        "rule_id": "CF_FUTURE_03",

        "current": [44],

        "target": 30,

        "gap": FUTURE,

        "severity": GAP_HIGH,

        "reason": "미래에 대한 긴장이 성장 욕구와 함께 나타난다.",
    },

    # ======================================================
    # PERFECTIONISM GAP
    # ======================================================

    {
        "rule_id": "CF_PERFECTIONISM_01",

        "current": [22],

        "target": 29,

        "gap": PERFECTIONISM,

        "severity": GAP_MEDIUM,

        "reason": "완벽을 추구하는 과정에서 성취감을 충분히 느끼지 못하고 있다.",
    },

    {
        "rule_id": "CF_PERFECTIONISM_02",

        "current": [11],

        "target": 29,

        "gap": PERFECTIONISM,

        "severity": GAP_LOW,

        "reason": "성과에 대한 자기 의심이 성취 욕구와 연결되고 있다.",
    },
]


#==========================================================================================================


# ==========================================================
# Confidence Rule
#
# Feature가 아니라
# 분석 결과 전체의 신뢰도를 계산한다.
# ==========================================================

CONFIDENCE_RULES = [

    # ======================================================
    # Reinforcement
    # ======================================================

    {
        "rule_id": "CFD_01",

        "requires_reinforcement": True,

        "score_delta": 10,

        "reason": "동일한 사고 패턴이 여러 질문에서 반복적으로 확인되었다.",
    },

    {
        "rule_id": "CFD_02",

        "requires_triple_reinforcement": True,

        "score_delta": 15,

        "reason": "동일한 심리 패턴이 세 개 이상의 질문에서 일관되게 나타났다.",
    },

    # ======================================================
    # Conflict
    # ======================================================

    {
        "rule_id": "CFD_03",

        "requires_conflict": True,

        "score_delta": 8,

        "reason": "현재 상태와 원하는 상태의 차이가 명확하게 확인되었다.",
    },

    # ======================================================
    # 응답 품질
    # ======================================================

    {
        "rule_id": "CFD_04",

        "required_questions": [
            2,
            3,
        ],

        "score_delta": 5,

        "reason": "핵심 사고 및 행동 질문에 모두 응답하였다.",
    },

    {
        "rule_id": "CFD_05",

        "required_questions": [
            4,
        ],

        "score_delta": 5,

        "reason": "목표 상태를 확인하여 Gap 분석이 가능하다.",
    },

    {
        "rule_id": "CFD_06",

        "required_questions": [
            5,
        ],

        "score_delta": 5,

        "reason": "실제 행동 데이터가 확보되어 행동 기반 분석이 가능하다.",
    },

    {
        "rule_id": "CFD_07",

        "required_questions": [
            6,
        ],

        "score_delta": 3,

        "reason": "현재 긴장의 원인이 확인되었다.",
    },

    # ======================================================
    # Feature 다양성
    # ======================================================

    {
        "rule_id": "CFD_08",

        "min_features": 2,

        "score_delta": 10,

        "reason": "여러 Feature가 함께 나타나 분석 근거가 풍부하다.",
    },

    {
        "rule_id": "CFD_09",

        "min_features": 4,

        "score_delta": 15,

        "reason": "다양한 사고 패턴이 확인되어 분석 신뢰도가 높다.",
    },

    # ======================================================
    # Feature 편향
    # ======================================================

    {
        "rule_id": "CFD_10",

        "single_feature_ratio": 0.80,

        "score_delta": -10,

        "reason": "하나의 Feature에 지나치게 편중되어 있다.",
    },

    # ======================================================
    # 기타(Other)
    # ======================================================

    {
        "rule_id": "CFD_11",

        "selected_options": [
            16,
            26,
            34,
            42,
            51,
        ],

        "threshold": 2,

        "score_delta": -15,

        "reason": "기타 응답 비율이 높아 규칙 기반 분석 근거가 감소하였다.",
    },

    # ======================================================
    # 없음(None)
    # ======================================================

    {
        "rule_id": "CFD_12",

        "selected_options": [
            15,
            25,
            50,
        ],

        "threshold": 2,

        "score_delta": -20,

        "reason": "응답 정보가 부족하여 분석 신뢰도가 감소하였다.",
    },

    {
        "rule_id": "CFD_13",

        "max_features": 1,

        "score_delta": -15,

        "reason": "관찰된 Feature가 지나치게 적어 분석 근거가 부족하다.",
    },

    {
        "rule_id": "CFD_14",

        "no_pattern": True,

        "score_delta": -10,

        "reason": "질문 간 일관된 패턴이 발견되지 않았다.",
    },

    {
        "rule_id": "CFD_15",

        "required_questions": [
            2,
            3,
            4,
            5,
            6,
        ],

        "score_delta": 5,

        "reason": "전체 온보딩 응답이 완료되어 분석 신뢰도가 향상되었다.",
    },

    {
        "rule_id": "CFD_16",

        "low_information": True,

        "score_delta": -25,

        "reason": "유효한 응답 정보가 부족하여 분석 신뢰도가 크게 감소하였다.",
    },
]



# ====================================================================================================
# ==========================================================
# Interpretation Rule
#
# Feature 결과를 사람이 이해할 수 있는
# 사고 패턴(Pattern)으로 변환한다.
#
# Feature
# ↓
# Pattern
#
# Seed 생성 전 단계
# ==========================================================

INTERPRETATION_RULES = [

    # ======================================================
    # Future Planner
    # ======================================================

    {
        "rule_id": "PT_FUTURE_01",

        "conditions": [
            {
                "feature":FUTURE,
                "operator":">=",
                "value":70,
            },

            {
            "feature":UNCERTAINTY,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern": "Future Planner",
        "pattern_code":"future_planner",

        "category":"Thinking",
        "priority": 100,
        "confidence":0.95,
        "evidence":[
            FUTURE,
            UNCERTAINTY
        ],

        "psychology":[
            "Future Orientation",
            "Intolerance of Uncertainty"
        ],

        "source":[
            CBT,
            KAHNEMAN
        ],

        "tags":[
            "future",
            "planning",
            "uncertainty"
        ],

        "growth_candidates":[
            "unlearning",
            "relearning",
            "newlearning"
        ],

        "identity_candidates":[
            "Strategic Builder"
        ],

        "os_candidates":[
            "Planner"
        ],

        "reason": "미래를 자주 시뮬레이션하며 장기적인 가능성을 고민하는 사고 패턴이다.",
    },

    # ======================================================
    # Action Blocker
    # ======================================================

    {
        "rule_id":"PT_EXECUTION_01",

        "conditions":[
            {
                "feature":EXECUTION,
                "operator":">=",
                "value":35,
            },
            {
                "feature":UNCERTAINTY,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Action Blocker",
        "pattern_code":"action_blocker",

        "category":"Action",

        "priority":95,
        "confidence":0.93,

        "evidence":[
            EXECUTION,
            UNCERTAINTY
        ],

        "psychology":[
            "Executive Dysfunction",
            "Analysis Paralysis"
        ],

        "source":[
            CBT,
            EXECUTIVE_FUNCTION
        ],

        "tags":[
            "execution",
            "delay",
            "planning"
        ],

        "growth_candidates":[
            "unlearning",
            "relearning",
            "newlearning"
        ],

        "identity_candidates":[
            "Planner"
        ],

        "os_candidates":[
            "Execution"
        ],

        "reason":"생각과 불확실성이 행동보다 앞서 실행이 반복적으로 지연되는 사고 패턴이다."
    },

    # ======================================================
    # Burned Executor
    # ======================================================

    {
        "rule_id":"PT_OVERLOAD_01",

        "conditions":[
            {
                "feature":OVERLOAD,
                "operator":">=",
                "value":70,
            },
            {
                "feature":RESILIENCE,
                "operator":"<=",
                "value":40,
            },
        ],

        "logic":"AND",

        "pattern":"Burned Executor",
        "pattern_code":"burned_executor",

        "category":"Recovery",

        "priority":95,
        "confidence":0.95,

        "evidence":[
            OVERLOAD,
            RESILIENCE
        ],

        "psychology":[
            "Mental Fatigue",
            "Recovery Theory"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "burnout",
            "fatigue",
            "overload"
        ],

        "growth_candidates":[
            "relearning",
            "newlearning"
        ],

        "identity_candidates":[
            "Persistent Builder"
        ],

        "os_candidates":[
            "Recovery"
        ],

        "reason":"과부하가 지속되어 회복보다 소모가 커진 상태이다."
    },

    # ======================================================
    # Perfection Seeker
    # ======================================================

    {
        "rule_id":"PT_PERFECTIONISM_01",

        "conditions":[
            {
                "feature":PERFECTIONISM,
                "operator":">=",
                "value":70,
            },
            {
                "feature":EXECUTION,
                "operator":"<=",
                "value":50,
            },
        ],

        "logic":"AND",

        "pattern":"Perfection Seeker",
        "pattern_code":"perfection_seeker",

        "category":"Thinking",

        "priority":90,
        "confidence":0.94,

        "evidence":[
            PERFECTIONISM,
            EXECUTION
        ],

        "psychology":[
            "Perfectionism"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "perfect",
            "delay"
        ],

        "growth_candidates":[
            "unlearning",
            "relearning"
        ],

        "identity_candidates":[
            "Quality Builder"
        ],

        "os_candidates":[
            "Quality"
        ],

        "reason":"완벽을 추구하지만 실행 속도가 함께 감소하는 사고 패턴이다."
    },

    # ======================================================
    # Creative Explorer
    # ======================================================

    {
        "rule_id":"PT_CREATIVITY_01",

        "conditions":[
            {
                "feature":CREATIVITY,
                "operator":">=",
                "value":75,
            },
            {
                "feature":FUTURE,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Creative Explorer",
        "pattern_code":"creative_explorer",

        "category":"Thinking",

        "priority":90,
        "confidence":0.92,

        "evidence":[
            CREATIVITY,
            FUTURE
        ],

        "psychology":[
            "Divergent Thinking"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "creative",
            "idea",
            "future"
        ],

        "growth_candidates":[
            "newlearning"
        ],

        "identity_candidates":[
            "Creator"
        ],

        "os_candidates":[
            "Creative"
        ],

        "reason":"새로운 아이디어를 미래 가능성과 연결하는 사고 패턴이다."
    },

    # ======================================================
    # Strategic Builder
    # ======================================================

    {
        "rule_id":"PT_EXECUTION_02",

        "conditions":[
            {
                "feature":EXECUTION,
                "operator":">=",
                "value":70,
            },
            {
                "feature":FUTURE,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Strategic Builder",
        "pattern_code":"strategic_builder",

        "category":"Growth",

        "priority":90,
        "confidence":0.94,

        "evidence":[
            EXECUTION,
            FUTURE
        ],

        "psychology":[
            "Goal Orientation"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "goal",
            "strategy"
        ],

        "growth_candidates":[
            "newlearning"
        ],

        "identity_candidates":[
            "Strategic Builder"
        ],

        "os_candidates":[
            "Planner"
        ],

        "reason":"장기적인 목표를 계획하고 실행으로 연결하는 경향이 높다."
    },

    # ======================================================
    # Self Doubter
    # ======================================================

    {
        "rule_id":"PT_UNCERTAINTY_01",

        "conditions":[
            {
                "feature":UNCERTAINTY,
                "operator":">=",
                "value":75,
            },
            {
                "feature":PERFECTIONISM,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Self Doubter",
        "pattern_code":"self_doubter",

        "category":"Thinking",

        "priority":88,
        "confidence":0.94,

        "evidence":[
            UNCERTAINTY,
            PERFECTIONISM
        ],

        "psychology":[
            "Self Efficacy"
        ],

        "source":[
            CBT,
            BANDURA
        ],

        "tags":[
            "self",
            "doubt"
        ],

        "growth_candidates":[
            "unlearning",
            "relearning"
        ],

        "identity_candidates":[
            "Reflective Builder"
        ],

        "os_candidates":[
            "Confidence"
        ],

        "reason":"자기 검증과 불확실성으로 인해 스스로를 자주 의심하는 경향이 있다."
    },

    # ======================================================
    # Growth Oriented
    # ======================================================

    {
        "rule_id":"PT_GROWTH_01",

        "conditions":[
            {
                "feature":FUTURE,
                "operator":">=",
                "value":65,
            },
            {
                "feature":EXECUTION,
                "operator":">=",
                "value":65,
            },
        ],

        "logic":"AND",

        "pattern":"Growth Oriented",
        "pattern_code":"growth_oriented",

        "category":"Growth",

        "priority":85,
        "confidence":0.90,

        "evidence":[
            FUTURE,
            EXECUTION
        ],

        "psychology":[
            "Growth Mindset"
        ],

        "source":[
            DWECK
        ],

        "tags":[
            "growth"
        ],

        "growth_candidates":[
            "newlearning"
        ],

        "identity_candidates":[
            "Growth Builder"
        ],

        "os_candidates":[
            "Growth"
        ],

        "reason":"성장을 장기적인 행동으로 연결하려는 사고 패턴이다."
    },

    # ======================================================
    # Recovery Needed
    # ======================================================

    {
        "rule_id":"PT_RESILIENCE_01",

        "conditions":[
            {
                "feature":OVERLOAD,
                "operator":">=",
                "value":65,
            },
            {
                "feature":RESILIENCE,
                "operator":"<=",
                "value":30,
            },
        ],

        "logic":"AND",

        "pattern":"Recovery Needed",
        "pattern_code":"recovery_needed",

        "category":"Recovery",

        "priority":90,
        "confidence":0.94,

        "evidence":[
            OVERLOAD,
            RESILIENCE
        ],

        "psychology":[
            "Recovery Theory"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "recovery"
        ],

        "growth_candidates":[
            "relearning",
            "newlearning"
        ],

        "identity_candidates":[
            "Persistent Builder"
        ],

        "os_candidates":[
            "Recovery"
        ],

        "reason":"현재 가장 필요한 것은 더 많은 실행보다 회복이다."
    },

    # ======================================================
    # Stable Thinker
    # ======================================================

    {
        "rule_id":"PT_STABLE_01",

        "conditions":[
            {
                "feature":UNCERTAINTY,
                "operator":"<=",
                "value":40,
            },
            {
                "feature":OVERLOAD,
                "operator":"<=",
                "value":40,
            },
            {
                "feature":RESILIENCE,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Stable Thinker",
        "pattern_code":"stable_thinker",

        "category":"Recovery",

        "priority":70,
        "confidence":0.88,

        "evidence":[
            UNCERTAINTY,
            OVERLOAD,
            RESILIENCE
        ],

        "psychology":[
            "Psychological Resilience"
        ],

        "source":[
            CBT
        ],

        "tags":[
            "stable",
            "balanced"
        ],

        "growth_candidates":[
            "newlearning"
        ],

        "identity_candidates":[
            "Balanced Builder"
        ],

        "os_candidates":[
            "Balance"
        ],

        "reason":"상대적으로 안정적인 사고 구조를 유지하고 있다."
    },
    

    # ======================================================
    # Analysis Paralysis
    # ======================================================

    {
        "rule_id":"PT_ANALYSIS_PARALYSIS_01",

        "conditions":[
            {
                "feature":EXECUTION,
                "operator":"<=",
                "value":35,
            },
            {
                "feature":UNCERTAINTY,
                "operator":">=",
                "value":70,
            },
            {
                "feature":OVERLOAD,
                "operator":">=",
                "value":60,
            },
        ],

        "logic":"AND",

        "pattern":"Analysis Paralysis",
        "pattern_code":"analysis_paralysis",

        "category":"Thinking",

        "priority":98,

        "confidence":0.97,

        "evidence":[
            EXECUTION,
            UNCERTAINTY,
            OVERLOAD,
        ],

        "psychology":[
            "Analysis Paralysis",
            "Intolerance of Uncertainty",
            "Executive Dysfunction",
        ],

        "source":[
            CBT,
            EXECUTIVE_FUNCTION,
            KAHNEMAN,
        ],

        "tags":[
            "overthinking",
            "analysis",
            "decision",
            "execution",
        ],

        "growth_candidates":[
            "unlearning",
            "relearning",
            "newlearning",
        ],

        "identity_candidates":[
            "Strategic Thinker",
        ],

        "os_candidates":[
            "Decision System",
        ],

        "reason":"생각과 불확실성이 반복적으로 행동보다 앞서면서 실행이 지연되는 사고 패턴이다.",
    },

    # ======================================================
    # Recovery First
    # ======================================================

    {
        "rule_id":"PT_RECOVERY_FIRST_01",

        "conditions":[
            {
                "feature":OVERLOAD,
                "operator":">=",
                "value":75,
            },
            {
                "feature":RESILIENCE,
                "operator":"<=",
                "value":30,
            },
        ],

        "logic":"AND",

        "pattern":"Recovery First",

        "pattern_code":"recovery_first",

        "category":"Recovery",

        "priority":97,

        "confidence":0.96,

        "evidence":[
            OVERLOAD,
            RESILIENCE,
        ],

        "psychology":[
            "Mental Fatigue",
            "Recovery Theory",
            "Burnout Prevention",
        ],

        "source":[
            CBT,
        ],

        "tags":[
            "recovery",
            "burnout",
            "fatigue",
            "rest",
        ],

        "growth_candidates":[
            "relearning",
            "newlearning",
        ],

        "identity_candidates":[
            "Sustainable Builder",
        ],

        "os_candidates":[
            "Recovery System",
        ],

        "reason":"현재 가장 필요한 것은 더 많은 실행이 아니라 충분한 회복이며, 회복 이후에 성과가 회복될 가능성이 높은 상태이다.",
    },
]