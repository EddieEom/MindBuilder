from dataclasses import dataclass


@dataclass
class NextAction:

    title: str

    description: str


@dataclass
class Recommendation:

    title: str

    description: str

    priority: int

    actions: list[NextAction]


@dataclass
class RecommendationResult:

    recommendations: list[Recommendation]

    confidence: float

    version: str