from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ======================================================
# NextAction Response DTO
# ======================================================

class NextActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    action_id: int
    recommendation_id: int
    title: str
    description: str | None = None
    status: str
    created_at: datetime


# ======================================================
# Recommendation Detail Response DTO
# ======================================================

class RecommendationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    recommendation_id: int
    pattern_id: int
    title: str
    description: str | None = None
    priority: int
    status: str
    created_at: datetime
    actions: list[NextActionResponse] = Field(
        default_factory=list,
        validation_alias="next_actions",
    )


# ======================================================
# Recommendation Generate / Current Response DTO
# ======================================================

class RecommendationGenerateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    pattern_id: int
    confidence: float
    recommendations: list[RecommendationDetailResponse] = Field(default_factory=list)
