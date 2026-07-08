from pydantic import BaseModel
from typing import Any

class PatternAnalysisResponse(BaseModel):

    pattern_id: int

    confidence: float

    scores: dict[str, float]

    patterns: list[dict]

    metadata: dict[str, Any]