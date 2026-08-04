from datetime import datetime
from pydantic import BaseModel, Field


class DashboardHumanOSResponse(BaseModel):
    stage: str
    confidence: float
    version: str


class DashboardInsightResponse(BaseModel):
    title: str
    content: str


class DashboardNextActionResponse(BaseModel):
    title: str
    action_type: str | None = None
    action_url: str | None = None


class DashboardChangeItemResponse(BaseModel):
    metric: str
    value: float
    change: float


class DashboardArchiveResponse(BaseModel):
    event_type: str
    title: str
    summary: str | None = None
    created_at: datetime


class DashboardResponse(BaseModel):

    human_os: DashboardHumanOSResponse

    insight: DashboardInsightResponse

    next_action: DashboardNextActionResponse

    recent_changes: list[DashboardChangeItemResponse] = Field(
        default_factory=list
    )

    recent_archives: list[DashboardArchiveResponse] = Field(
        default_factory=list
    )