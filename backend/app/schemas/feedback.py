from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):

    rating: int = Field(
        ge=1,
        le=5,
    )

    comment: str | None = None


class FeedbackResponse(BaseModel):

    feedback_id: int

    rating: int

    comment: str | None = None

    message: str