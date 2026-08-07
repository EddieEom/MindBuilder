from pydantic import BaseModel


class NextActionSchema(BaseModel):

    title: str

    description: str


class RecommendationSchema(BaseModel):

    title: str

    description: str

    priority: int

    actions: list[NextActionSchema]


class RecommendationOutputSchema(BaseModel):

    recommendations: list[RecommendationSchema]

    confidence: float