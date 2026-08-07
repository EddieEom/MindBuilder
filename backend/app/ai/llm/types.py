from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


# ==========================================================
# Usage
# ==========================================================

@dataclass(slots=True)
class TokenUsage:

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int


# ==========================================================
# Metadata
# ==========================================================

@dataclass(slots=True)
class GenerationMetadata:

    model: str

    latency: float

    retry_count: int

    success: bool


# ==========================================================
# Response
# ==========================================================

@dataclass(slots=True)
class LLMResponse:

    raw_text: str

    parsed: dict[str, Any]

    validated: BaseModel

    metadata: GenerationMetadata

    usage: TokenUsage | None = None