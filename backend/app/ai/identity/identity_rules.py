# app/ai/identity/identity_rules.py

IDENTITY_RULES = [

    {
        "rule_id": "ID_BUILDER",
        "identity_key": "builder",
        "identity_name": "Builder",
        "description": (
            "Turns insight into concrete systems, projects, and repeatable progress."
        ),
        "score_weights": {
            "pattern": {
                "execution_score": 0.35,
                "creativity_score": 0.25,
            },
            "trend": 0.20,
            "growth": 0.20,
        },
        "trend_metrics": [
            "execution_score",
            "creativity_score",
        ],
        "stable_metrics": [
            "execution_score",
            "creativity_score",
        ],
        "keywords": [
            "execution",
            "creation",
            "systems",
            "iteration",
        ],
        "strengths": [
            "Connects ideas to practical action.",
            "Builds repeatable structures from loose signals.",
            "Improves through evidence and iteration.",
        ],
        "growth_points": [
            "Protect execution priorities from over-expansion.",
            "Keep experiments small enough to finish.",
            "Review pattern changes before redefining direction.",
        ],
    },

    {
        "rule_id": "ID_EXPLORER",
        "identity_key": "explorer",
        "identity_name": "Explorer",
        "description": (
            "Searches widely, connects possibilities, and learns through discovery."
        ),
        "score_weights": {
            "pattern": {
                "future_score": 0.30,
                "creativity_score": 0.25,
                "resilience_score": 0.05,
            },
            "trend": 0.20,
            "growth": 0.20,
        },
        "trend_metrics": [
            "future_score",
            "creativity_score",
        ],
        "stable_metrics": [
            "future_score",
            "creativity_score",
        ],
        "keywords": [
            "curiosity",
            "possibility",
            "learning",
            "discovery",
        ],
        "strengths": [
            "Finds new directions quickly.",
            "Learns by testing unfamiliar paths.",
            "Keeps multiple possibilities visible.",
        ],
        "growth_points": [
            "Turn exploration into a small next action.",
            "Limit active options before energy diffuses.",
            "Use pattern history to separate signal from novelty.",
        ],
    },

    {
        "rule_id": "ID_CREATOR",
        "identity_key": "creator",
        "identity_name": "Creator",
        "description": (
            "Generates original ideas and turns inner material into visible output."
        ),
        "score_weights": {
            "pattern": {
                "creativity_score": 0.45,
                "future_score": 0.15,
                "execution_score": 0.10,
            },
            "trend": 0.15,
            "growth": 0.15,
        },
        "trend_metrics": [
            "creativity_score",
            "execution_score",
        ],
        "stable_metrics": [
            "creativity_score",
        ],
        "keywords": [
            "originality",
            "expression",
            "ideation",
            "making",
        ],
        "strengths": [
            "Produces fresh connections from raw input.",
            "Transforms abstract ideas into expressive work.",
            "Uses imagination as a problem-solving tool.",
        ],
        "growth_points": [
            "Attach each idea to a delivery rhythm.",
            "Keep quality standards from blocking output.",
            "Build a capture system for recurring ideas.",
        ],
    },

    {
        "rule_id": "ID_LEADER",
        "identity_key": "leader",
        "identity_name": "Leader",
        "description": (
            "Creates direction, mobilizes action, and keeps momentum under pressure."
        ),
        "score_weights": {
            "pattern": {
                "execution_score": 0.40,
                "resilience_score": 0.20,
                "future_score": 0.10,
            },
            "trend": 0.15,
            "growth": 0.15,
        },
        "trend_metrics": [
            "execution_score",
            "resilience_score",
        ],
        "stable_metrics": [
            "execution_score",
            "resilience_score",
        ],
        "keywords": [
            "direction",
            "momentum",
            "decision",
            "responsibility",
        ],
        "strengths": [
            "Moves from ambiguity toward action.",
            "Maintains direction when pressure rises.",
            "Creates momentum for people and projects.",
        ],
        "growth_points": [
            "Balance speed with recovery capacity.",
            "Make decision criteria explicit.",
            "Use reflection before taking on more responsibility.",
        ],
    },

    {
        "rule_id": "ID_RESEARCHER",
        "identity_key": "researcher",
        "identity_name": "Researcher",
        "description": (
            "Investigates deeply, compares evidence, and refines understanding over time."
        ),
        "score_weights": {
            "pattern": {
                "future_score": 0.25,
                "perfectionism_score": 0.25,
                "creativity_score": 0.15,
            },
            "trend": 0.15,
            "growth": 0.20,
        },
        "trend_metrics": [
            "future_score",
            "perfectionism_score",
        ],
        "stable_metrics": [
            "future_score",
            "perfectionism_score",
        ],
        "keywords": [
            "analysis",
            "evidence",
            "depth",
            "refinement",
        ],
        "strengths": [
            "Looks for underlying causes.",
            "Improves thinking through evidence.",
            "Notices inconsistencies that others may miss.",
        ],
        "growth_points": [
            "Convert research into a decision point.",
            "Define enough evidence before investigating more.",
            "Watch for perfectionism delaying movement.",
        ],
    },

    {
        "rule_id": "ID_ARCHITECT",
        "identity_key": "architect",
        "identity_name": "Architect",
        "description": (
            "Designs coherent structures that align goals, systems, and long-term direction."
        ),
        "score_weights": {
            "pattern": {
                "future_score": 0.30,
                "execution_score": 0.25,
                "creativity_score": 0.15,
            },
            "trend": 0.15,
            "growth": 0.15,
        },
        "trend_metrics": [
            "future_score",
            "execution_score",
        ],
        "stable_metrics": [
            "future_score",
            "execution_score",
            "creativity_score",
        ],
        "keywords": [
            "structure",
            "strategy",
            "systems",
            "alignment",
        ],
        "strengths": [
            "Sees the relationship between parts and direction.",
            "Creates structure for complex problems.",
            "Builds systems that can evolve over time.",
        ],
        "growth_points": [
            "Validate the system with small user-facing actions.",
            "Avoid redesigning before enough pattern data changes.",
            "Keep architecture connected to daily execution.",
        ],
    },

]
