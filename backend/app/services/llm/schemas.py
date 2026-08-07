from pydantic import BaseModel


class LLMAnalysisResponse(
    BaseModel,
):

    identity_summary: str

    strengths: list[str]

    growth_points: list[str]