from typing import Any

from pydantic import BaseModel, Field
from datetime import datetime

class OSCoreValueResponse(BaseModel):
    value_name: str
    description: str | None = None
    priority: int


class OperatingSystemResponse(BaseModel):
    os_id: int
    version: str
    stage: str
    data_confidence: str
    core_values: list[OSCoreValueResponse]
    thinking_pattern: str
    decision_pattern: str
    operating_rules: list[str]
    metadata: dict[str, Any] = Field(default_factory=dict)


class OperatingSystemHistoryResponse(BaseModel):
    operating_systems: list[OperatingSystemResponse]


# ======================================================
# Version
# ======================================================

class OperatingSystemVersionResponse(BaseModel):

    os_id: int

    version: str

    stage: str

    generated_at: datetime

    is_current: bool