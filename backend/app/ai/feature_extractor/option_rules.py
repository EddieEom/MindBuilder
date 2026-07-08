# 옵션별 가중치
# 이 파일은 "옵션 하나가 어떤 Feature에 얼마나 영향을 주는가" 만 정의한다.


from app.ai.feature_extractor.constants import (
    FUTURE,
    EXECUTION,
    CREATIVITY,
    UNCERTAINTY,
    PERFECTIONISM,
    RESILIENCE,
    WEAK,
    MEDIUM,
    STRONG,
    OVERLOAD,
    THINKING_PATTERN,
    STRESS_PATTERN,
    SELF_EVALUATION,
    CBT,
    EXECUTIVE_FUNCTION,
)

"""
MindBuilder Rule Engine

Option Rule

Raw Data
↓

Feature Extraction

※ 여기서는
'직접적으로 측정 가능한 Feature'만 정의한다.

Q1, Q5는 Feature 계산에서 제외한다.
(Q1 : 관심사 / Q5 : 실제 행동)
→ Cross Rule과 Identity에서 활용한다.
"""

# ==========================================================
# Q2. 최근 당신을 가장 자주 고민하게 만드는 것은 무엇인가요?
# ==========================================================

Q2_OPTION_RULES = {

    # ------------------------------------------------------
    # 무엇부터 해야 할지 모르겠다.
    # ------------------------------------------------------

    8: [

        {
            "rule_id": "Q2_08_01",

            "feature": EXECUTION,
            "weight": STRONG,
            "reason": "우선순위를 결정하지 못해 실행이 지연되고 있다.",
            "confidence": 0.90,
            "priority":100,
            "category": THINKING_PATTERN,
        },

        {   
            "rule_id": "Q2_08_02",
            "feature": UNCERTAINTY,
            "weight": MEDIUM,
            "reason": "올바른 선택에 대한 확신이 부족하다.",
            "confidence": 0.75,
            "priority":70,
            "category": THINKING_PATTERN,
        },

    ],

    # ------------------------------------------------------
    # 해야 할 일이 너무 많다.
    # ------------------------------------------------------

    9: [

        {   
            "rule_id": "Q2_09_01",

            "feature": OVERLOAD,
            "weight": STRONG,
            "reason": "인지 부하가 높아 작업 기억에 부담이 발생하고 있다.",
            "confidence": 0.97,
            "priority":100,
            "category": STRESS_PATTERN,
        },

    ],

    # ------------------------------------------------------
    # 미래에 대한 생각이 자주 난다.
    # ------------------------------------------------------

    10: [

        {   
            "rule_id": "Q2_10_01",

            "feature": FUTURE,
            "weight": STRONG,
            "reason": "미래를 중심으로 사고하는 경향이 높다.",
            "confidence": 0.95,
            "priority":100,
            "category": "thinking_pattern",
        },

        {   
            "rule_id": "Q2_10_02",

            "feature": UNCERTAINTY,
            "weight": WEAK,
            "confidence": 0.45,
            "priority":40,
            "reason": "미래에 대한 불확실성을 함께 인식하고 있다.",
            "category": THINKING_PATTERN,
        },

    ],

    # ------------------------------------------------------
    # 잘하고 있는지 의심하게 된다.
    # ------------------------------------------------------

    11: [

        {   
            "rule_id": "Q2_11_01",

            "feature": UNCERTAINTY,
            "weight": STRONG,
            "reason": "현재 자신의 판단과 성과를 신뢰하지 못하고 있다.",
            "confidence": 0.92,
            "priority":100,
            "category": SELF_EVALUATION,
        },

        {   
            "rule_id": "Q2_11_02",

            "feature": PERFECTIONISM,
            "weight": WEAK,
            "reason": "스스로에게 자기 검증을 반복하려는 경향이 있다.",
            "confidence": 0.55,
            "priority":60,
            "category": SELF_EVALUATION,
        },

    ],

    # ------------------------------------------------------
    # 다른 사람과 비교하게 된다.
    # ------------------------------------------------------

    12: [

        {   
            "rule_id": "Q2_12_01",

            "feature": UNCERTAINTY,
            "weight": WEAK,
            "reason": "외부 기준을 통해 자신의 위치를 판단하려는 경향이 있다.",
            "confidence": 0.70,
            "priority":70,
            "category": SELF_EVALUATION,
        },

        {   
            "rule_id": "Q2_12_02",

            "feature": PERFECTIONISM,
            "weight": WEAK,
            "reason": "타인의 기준을 자신의 목표 수준으로 받아들이고 있다.",
            "confidence": 0.60,
            "priority":50,
            "category": SELF_EVALUATION,
        },

    ],

    # ------------------------------------------------------
    # 쉬어야 하는데 쉬지 못한다.
    # ------------------------------------------------------

    13: [

        {   
            "rule_id": "Q2_13_01",

            "feature": OVERLOAD,
            "weight": STRONG,
            "reason": "충분한 회복 없이 지속적으로 에너지를 소비하고 있다.",
            "confidence": 0.93,
            "priority":100,
            "category": STRESS_PATTERN,
        },

        {
            "rule_id": "Q2_13_02",


            "feature": RESILIENCE,
            "weight": WEAK,
            "reason": "회복 행동이 부족하여 장기적인 회복 능력이 저하될 가능성이 있다.",
            "confidence": 0.50,
            "priority":60,
            "category": STRESS_PATTERN,
        },

    ],

    # ------------------------------------------------------
    # 새로운 아이디어가 계속 떠오른다.
    # ------------------------------------------------------

    14: [

        {   
            "rule_id": "Q2_14_01",

            "feature": CREATIVITY,
            "weight": STRONG,
            "reason": "새로운 아이디어를 지속적으로 연결하는 사고가 나타난다.",
            "confidence": 0.95,
            "priority":100,
            "psychology": "Divergent Thinking",
            "tags":[
                "creative",
                "idea",
                "divergent"
            ]
        },

    ],

    # ------------------------------------------------------
    # 특별히 없다.
    # ------------------------------------------------------

    15: [],

    # ------------------------------------------------------
    # 기타
    # ------------------------------------------------------

    16: [],
}



# ==========================================================
# Q3. 최근 당신의 행동 속도를 가장 느리게 만드는 것은 무엇인가요?
# ==========================================================

Q3_OPTION_RULES = {

    # ------------------------------------------------------
    # 생각이 너무 많다.
    # ------------------------------------------------------

    17: [

        {   
            "rule_id": "Q3_17_01",

            "feature": UNCERTAINTY,
            "weight": STRONG,
            "confidence": 0.93,
            "reason": "과도한 사고가 의사결정을 지연시키고 있다.",
            "priority":100,
            "psychology": "Analysis Paralysis",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_17_02",

            "feature": EXECUTION,
            "weight": MEDIUM,
            "confidence": 0.82,
            "reason": "생각이 많아 실제 행동으로 이어지기 어렵다.",
            "priority":100,
            "psychology": "Analysis Paralysis",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 무엇부터 해야 할지 모르겠다.
    # ------------------------------------------------------

    18: [

        {   
            "rule_id": "Q3_18_01",

            "feature": EXECUTION,
            "weight": STRONG,
            "confidence": 0.95,
            "reason": "우선순위를 정하지 못해 행동을 시작하지 못한다.",
            "priority":100,
            "psychology": "Executive Dysfunction",
            "evidence":"strong",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_18_02",

            "feature": UNCERTAINTY,
            "weight": MEDIUM,
            "confidence": 0.78,
            "reason": "올바른 선택에 대한 확신이 부족하다.",
            "priority":70,
            "psychology": "Decision Paralysis",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 시간이 부족하다.
    # ------------------------------------------------------

    19: [

        {   
            "rule_id": "Q3_19_01",

            "feature": OVERLOAD,
            "weight": STRONG,
            "confidence": 0.91,
            "reason": "시간 부족으로 인해 인지적 부담이 증가하고 있다.",
            "priority":100,
            "psychology": "Time Pressure",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_19_02",


            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.60,
            "reason": "시간 제약으로 실행 빈도가 감소하고 있다.",
            "priority":50,
            "psychology": "Time Pressure",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 에너지가 부족하다.
    # ------------------------------------------------------

    20: [

        {   
            "rule_id": "Q3_20_01",

            "feature": OVERLOAD,
            "weight": STRONG,
            "confidence": 0.94,
            "reason": "지속적인 에너지 소모로 회복이 충분하지 않은 상태이다.",
            "priority":100,
            "psychology": "Mental Fatigue",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_20_02",

            "feature": RESILIENCE,
            "weight": WEAK,
            "direction": "negative",
            "confidence": 0.55,
            "reason": "회복 능력이 일시적으로 저하될 가능성이 있다.",
            "priority":40,
            "psychology": "Recovery",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
            "tags":[
                "recovery",
                "fatigue",
                "rest",
            ]
        },

    ],

    # ------------------------------------------------------
    # 불안하다.
    # ------------------------------------------------------

    21: [

        {   
            "rule_id": "Q3_21_01",

            "feature": UNCERTAINTY,
            "weight": STRONG,
            "confidence": 0.96,
            "reason": "불확실성을 크게 인식하여 행동을 주저하고 있다.",
            "priority":100,
            "psychology": "Intolerance of Uncertainty",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_21_02",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.60,
            "reason": "불안이 행동 개시를 방해하고 있다.",
            "priority":50,
            "psychology": "Behavioral Inhibition",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 완벽하게 하고 싶다.
    # ------------------------------------------------------

    22: [

        {   
            "rule_id": "Q3_22_01",

            "feature": PERFECTIONISM,
            "weight": STRONG,
            "confidence": 0.98,
            "reason": "높은 완성도를 추구하여 행동을 미루는 경향이 있다.",
            "priority":100,
            "psychology": "Perfectionism",
            "evidence":"strong",
            "category": SELF_EVALUATION,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

        {   
            "rule_id": "Q3_22_02",

            "feature": EXECUTION,
            "weight": MEDIUM,
            "confidence": 0.80,
            "reason": "완벽주의로 인해 실행이 지연되고 있다.",
            "priority":100,
            "psychology": "Perfectionism",
            "evidence":"strong",
            "category": SELF_EVALUATION,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 집중력이 자주 끊긴다.
    # ------------------------------------------------------

    23: [

        {   
            "rule_id": "Q3_23_01",

            "feature": EXECUTION,
            "weight": STRONG,
            "confidence": 0.90,
            "reason": "지속적인 집중이 어려워 행동을 유지하기 어렵다.",
            "priority":100,
            "psychology": "Sustained Attention",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ]
        },

    ],

    # ------------------------------------------------------
    # 계획이 없다.
    # ------------------------------------------------------

    24: [

        {   
            "rule_id": "Q3_24_01",

            "feature": EXECUTION,
            "weight": STRONG,
            "confidence": 0.94,
            "reason": "행동 계획이 없어 실행이 체계적으로 이루어지지 않는다.",
            "priority":100,
            "psychology": "Planning",
            "evidence":"strong",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
            "tags":[
                "planning",
                "priority",
                "decision",
            ]
        },

    ],

    # ------------------------------------------------------
    # 특별히 없다.
    # ------------------------------------------------------

    25: [],

    # ------------------------------------------------------
    # 기타
    # ------------------------------------------------------

    26: [],
}


# ==========================================================
# Q4. 지금 당신이 가장 얻고 싶은 상태는 무엇인가요?
# ==========================================================

Q4_OPTION_RULES = {

    # ------------------------------------------------------
    # 명확한 방향
    # ------------------------------------------------------

    27: [

        {   
            "rule_id": "Q4_27_01",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.70,
            "reason": "행동 방향에 대한 명확성을 원하고 있다.",
            "priority":70,
            "psychology": "Goal Orientation",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 마음의 안정감
    # ------------------------------------------------------

    28: [

        {   
            "rule_id": "Q4_28_01",

            "feature": RESILIENCE,
            "weight": WEAK,
            "confidence": 0.55,
            "direction": "negative",
            "reason": "현재 심리적 안정감이 부족하다고 느끼고 있다.",
            "priority":50,
            "psychology": "Emotional Regulation",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 성취감
    # ------------------------------------------------------

    29: [

        {   
            "rule_id": "Q4_29_01",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.74,
            "reason": "행동을 통해 성과를 얻고 싶은 욕구가 높다.",
            "priority":70,
            "psychology": "Achievement Motivation",
            "category": SELF_EVALUATION,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 성장감
    # ------------------------------------------------------

    30: [

        {   
            "rule_id": "Q4_30_01",

            "feature": FUTURE,
            "weight": WEAK,
            "confidence": 0.78,
            "reason": "장기적인 성장과 발전을 중요하게 생각한다.",
            "priority":70,
            "psychology": "Growth Mindset",
            "evidence":"moderate",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 휴식
    # ------------------------------------------------------

    31: [

        {   
            "rule_id": "Q4_31_01",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.55,
            "direction": "negative",
            "reason": "회복 부족으로 실행 지속성이 감소하고 있다.",
            "priority":40,
            "psychology": "Mental Fatigue",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 자유
    # ------------------------------------------------------

    32: [

        {   
            "rule_id": "Q4_32_01",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.50,
            "reason": "자율적인 선택과 행동을 원한다.",
            "priority":40,
            "psychology": "Self-Determination Theory",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 자신감
    # ------------------------------------------------------

    33: [

        {   
            "rule_id": "Q4_33_01",

            "feature": UNCERTAINTY,
            "weight": WEAK,
            "confidence": 0.75,
            "direction": "negative",
            "reason": "현재 자신의 판단에 대한 확신을 높이고 싶어한다.",
            "priority":70,
            "psychology": "Self-Efficacy",
            "category": SELF_EVALUATION,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 기타
    # ------------------------------------------------------

    34: [],
}



# ==========================================================
# Q6. 최근 당신의 긴장을 가장 크게 만드는 것은 무엇인가요?
# ==========================================================

Q6_OPTION_RULES = {

    # ------------------------------------------------------
    # 커리어
    # ------------------------------------------------------

    43: [

        {
            "rule_id": "Q6_43_01",

            "feature": UNCERTAINTY,
            "weight": WEAK,
            "confidence":0.73,
            "reason": "진로 및 직업과 관련된 미래를 중요하게 인식하고 있다.",
            "priority":70,
            "psychology": "Future Orientation",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 미래
    # ------------------------------------------------------

    44: [

        {   
            "rule_id": "Q6_44_01",

            "feature": FUTURE,
            "weight": MEDIUM,
            "confidence": 0.90,
            "reason": "미래에 대한 불확실성이 현재 긴장의 주요 원인이다.",
            "priority":100,
            "psychology": "Future Anxiety",
            "category": THINKING_PATTERN,
            "tags":[
                "uncertainty",
                "avoidance",
                "future",
            ],
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

        {   
            "rule_id": "Q6_44_02",

            "feature": UNCERTAINTY,
            "weight": MEDIUM,
            "confidence": 0.87,
            "reason": "예측하기 어려운 미래를 부담스럽게 인식하고 있다.",
            "priority":100,
            "psychology": "Intolerance of Uncertainty",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 돈
    # ------------------------------------------------------

    45: [

        {   
            "rule_id": "Q6_45_01",

            "feature": UNCERTAINTY,
            "weight": WEAK,
            "confidence": 0.75,
            "reason": "경제적 안정성에 대한 불확실성을 경험하고 있다.",
            "priority":70,
            "psychology": "Financial Stress",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 프로젝트
    # ------------------------------------------------------

    46: [

        {   
            "rule_id": "Q6_46_01",

            "feature": OVERLOAD,
            "weight": WEAK,
            "confidence": 0.74,
            "reason": "현재 수행 중인 프로젝트가 인지적 부담을 만들고 있다.",
            "priority":70,
            "psychology": "Cognitive Load",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

        {   
            "rule_id": "Q6_46_02",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence":0.64,
            "reason":"프로젝트 수행 과정에서 행동 수행 부담을 경험하고 있다.",
            "priority":60,
            "psychology":"Performance Pressure",
            "category":THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        }

    ],

    # ------------------------------------------------------
    # 인간관계
    # ------------------------------------------------------

    47: [

        {   
            "rule_id": "Q6_47_01",

            "feature": RESILIENCE,
            "weight": WEAK,
            "confidence": 0.60,
            "direction": "negative",
            "reason": "대인관계에서 심리적 소모를 경험하고 있다.",
            "priority":50,
            "psychology": "Interpersonal Stress",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 건강
    # ------------------------------------------------------

    48: [

        {   
            "rule_id": "Q6_48_01",

            "feature": RESILIENCE,
            "weight": WEAK,
            "confidence": 0.62,
            "direction": "negative",
            "reason": "신체적·심리적 회복 상태에 대한 우려가 존재한다.",
            "priority":60,
            "psychology": "Health Anxiety",
            "evidence":"moderate",
            "category": STRESS_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
            "tags":[
                "uncertainty",
                "avoidance",
                "future",
            ]
        },

    ],

    # ------------------------------------------------------
    # 학업
    # ------------------------------------------------------

    49: [

        {   
            "rule_id": "Q6_49_01",

            "feature": EXECUTION,
            "weight": WEAK,
            "confidence": 0.68,
            "reason": "학업 성과가 미래와 연결된다고 인식하고 있다.",
            "priority":60,
            "psychology": "Achievement Motivation",
            "category": THINKING_PATTERN,
            "source":[
                CBT,
                EXECUTIVE_FUNCTION,
            ],
        },

    ],

    # ------------------------------------------------------
    # 없음
    # ------------------------------------------------------

    50: [],

    # ------------------------------------------------------
    # 기타
    # ------------------------------------------------------

    51: [],
}


OPTION_RULES = {

    2: Q2_OPTION_RULES,
    3: Q3_OPTION_RULES,
    4: Q4_OPTION_RULES,
    6: Q6_OPTION_RULES,
}

