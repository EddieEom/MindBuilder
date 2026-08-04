from pydantic import BaseModel
from typing import Any

from app.schemas.growth import (
    GrowthResponse,
)

from app.schemas.identity import (
    IdentityResponse,
)


class PatternAnalysisResponse(BaseModel):

    pattern_id: int

    confidence: float

    scores: dict

    patterns: list

    metadata: dict

    growth: GrowthResponse

    identity: IdentityResponse