from typing import Any, Literal

from pydantic import BaseModel, Field


class IdentityResponse(BaseModel):

    identity_name: str

    description: str

    confidence: float

    creativity_score: int

    execution_score: int

    uncertainty_score: int

    keywords: list[str]

    strengths: list[str]

    growth_points: list[str]

    identity_scores: dict[str, float] = Field(
        default_factory=dict
    )

    ranking: list[dict[str, Any]] = Field(
        default_factory=list
    )

    primary_identity: str = ""

    secondary_identity: str = ""

    score_gap: float = 0.0

    matched_rules: list[dict[str, Any]] = Field(
        default_factory=list
    )

    evidence: dict[str, Any] = Field(
        default_factory=dict
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    warnings: list[str] = Field(
        default_factory=list
    )

    candidates: list[dict[str, Any]] = Field(default_factory=list)
    hypothesis_status: str = "INSUFFICIENT"
    feedback: dict[str, Any] | None = None
    user_perspective: dict[str, Any] | None = None


class IdentityFeedbackRequest(BaseModel):
    agreement: Literal["AGREE", "PARTIAL", "DISAGREE", "UNSURE"]
    correction_text: str | None = Field(default=None, max_length=1000)


class IdentityFeedbackResponse(BaseModel):
    feedback_id: int
    identity_id: int
    agreement: str
    correction_text: str | None = None
    updated_at: Any
