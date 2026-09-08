from pydantic import BaseModel, Field, field_validator


class UserSettingsResponse(BaseModel):
    dark_mode: bool
    language: str
    notifications_enabled: bool
    reminder_hour: int
    timezone: str


class UserSettingsUpdate(BaseModel):
    dark_mode: bool | None = None
    language: str | None = None
    notifications_enabled: bool | None = None
    reminder_hour: int | None = Field(None, ge=0, le=23)
    timezone: str | None = Field(None, min_length=1, max_length=64)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str | None) -> str | None:
        if value is not None and value not in {"ko", "en"}:
            raise ValueError("language must be ko or en")
        return value


class ScanReminderResponse(BaseModel):
    should_notify: bool
    notification_id: int | None = None
    title: str | None = None
    content: str | None = None
    confidence: int
