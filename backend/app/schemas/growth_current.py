from datetime import datetime

from pydantic import BaseModel, Field


# ======================================================
# Growth Item
# ======================================================

class GrowthCurrentItemResponse(BaseModel):

    type: str

    title: str

    content: str

    priority: int


# ======================================================
# Recommendation
# ======================================================

class GrowthCurrentRecommendationResponse(BaseModel):

    title: str

    description: str

    priority: int


# ======================================================
# Feedback
# ======================================================

class GrowthCurrentFeedbackResponse(BaseModel):

    rating: int

    comment: str | None = None


# ======================================================
# Metadata
# ======================================================

class GrowthCurrentMetadataResponse(BaseModel):

    growth_analysis_id: int

    analysis_version: str

    llm_model: str

    confidence: float

    created_at: datetime


# ======================================================
# Current Growth Response
# ======================================================

class GrowthCurrentResponse(BaseModel):

    items: list[GrowthCurrentItemResponse] = Field(
        default_factory=list
    )

    recommendations: list[
        GrowthCurrentRecommendationResponse
    ] = Field(
        default_factory=list
    )

    feedback: GrowthCurrentFeedbackResponse | None = None

    metadata: GrowthCurrentMetadataResponse