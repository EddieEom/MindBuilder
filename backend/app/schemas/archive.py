from datetime import datetime
from pydantic import BaseModel


class ArchiveEventResponse(BaseModel):
    event_id: int
    user_id: int
    event_type: str
    reference_id: int
    title: str
    summary: str | None = None
    created_at: datetime


class ArchiveListResponse(BaseModel):
    events: list[ArchiveEventResponse]
