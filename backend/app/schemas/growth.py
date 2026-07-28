from pydantic import BaseModel
from typing import Any

# ======================================================
# Unlearning
# ======================================================

class UnlearningResponse(BaseModel):

    title: str
    thinking_pattern: str
    core_belief: str
    description: str
    confidence: float


# ======================================================
# Relearning
# ======================================================

class RelearningResponse(BaseModel):

    title: str
    root_cause: str
    mechanism: str
    description: str
    confidence: float


# ======================================================
# Newlearning
# ======================================================

class NewlearningResponse(BaseModel):

    title: str
    new_belief: str
    action: str
    habit: str
    description: str
    confidence: float


# ======================================================
# AI Explanation
# ======================================================

class ExplanationResponse(BaseModel):

    title: str
    content: str
    confidence: float


# ======================================================
# Recommendation
# ======================================================

class RecommendationResponse(BaseModel):

    title: str
    description: str
    priority: int


# ======================================================
# Feedback
# ======================================================

class FeedbackResponse(BaseModel):

    rating: int
    comment: str | None = None

# ======================================================
# Growth Response
# ======================================================


class GrowthItem(BaseModel):

    title: str

    content: str

    evidence: list[Any] = []


class GrowthResponse(BaseModel):

    unlearning: dict | None = None

    relearning: dict | None = None

    newlearning: dict | None = None

    explanations: list[dict] = []

    recommendations: list[dict] = []

    feedback: dict = {}

    metadata: dict = {}

    warnings: list[str] = []