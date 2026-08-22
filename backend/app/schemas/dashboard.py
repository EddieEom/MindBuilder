from datetime import datetime
from pydantic import BaseModel, Field


class DashboardHumanOSResponse(BaseModel):
    stage: str | None = None
    confidence: float | None = None
    version: str | None = None


class DashboardInsightResponse(BaseModel):
    title: str | None = None
    content: str | None = None


class DashboardNextActionResponse(BaseModel):
    title: str | None = None
    action_type: str | None = None
    action_url: str | None = None


class DashboardChangeItemResponse(BaseModel):
    metric: str
    value: float
    change: float | None = None


class DashboardArchiveResponse(BaseModel):
    event_type: str
    title: str
    summary: str | None = None
    created_at: datetime


class DashboardResponse(BaseModel):

    human_os: DashboardHumanOSResponse | None = None

    insight: DashboardInsightResponse | None = None

    next_action: DashboardNextActionResponse | None = None

    recent_changes: list[DashboardChangeItemResponse] = Field(
        default_factory=list
    )

    recent_archives: list[DashboardArchiveResponse] = Field(
        default_factory=list
    )
