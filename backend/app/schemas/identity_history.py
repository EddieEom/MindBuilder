from datetime import datetime

from pydantic import BaseModel


class IdentityHistoryItemResponse(BaseModel):

    identity_id: int

    identity_name: str

    version: int

    confidence: float

    generated_at: datetime

    is_current: bool


class IdentityHistoryResponse(BaseModel):

    histories: list[
        IdentityHistoryItemResponse
    ]