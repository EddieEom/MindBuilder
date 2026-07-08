from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StartOnboardingResponse(BaseModel):
    scan_id: int
    status: str
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)