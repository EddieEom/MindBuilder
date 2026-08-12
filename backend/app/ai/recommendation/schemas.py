from pydantic import BaseModel, Field

class NextActionSchema(BaseModel):

    title: str

    description: str


class RecommendationSchema(BaseModel):

    title: str

    description: str

    priority: int

    actions: list[NextActionSchema] = Field(
        min_length=2,
        max_length=2,
    )


class RecommendationOutputSchema(BaseModel):

    recommendations: list[RecommendationSchema] = Field(
        min_length=3,
        max_length=3,
    )

    confidence: float

    