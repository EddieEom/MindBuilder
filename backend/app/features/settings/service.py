from datetime import datetime, time, timedelta, timezone

from .repository import SettingsRepository
from .schemas import ScanReminderResponse, UserSettingsResponse, UserSettingsUpdate


class SettingsService:
    def __init__(self, repository: SettingsRepository):
        self.repository = repository

    async def get(self, user_id: int) -> UserSettingsResponse:
        settings = await self.repository.get_or_create(user_id)
        await self.repository.commit()
        return self._response(settings)

    async def update(self, user_id: int, payload: UserSettingsUpdate) -> UserSettingsResponse:
        settings = await self.repository.get_or_create(user_id)
        values = payload.model_dump(exclude_unset=True)
        if "timezone" in values and values["timezone"] not in {"Asia/Seoul", "UTC"}:
            raise ValueError("timezone must be Asia/Seoul or UTC")
        for key, value in values.items():
            setattr(settings, key, value)
        await self.repository.commit()
        return self._response(settings)

    async def check_scan_reminder(self, user_id: int, now: datetime | None = None) -> ScanReminderResponse:
        settings = await self.repository.get_or_create(user_id)
        confidence = await self.repository.confidence(user_id)
        if not settings.notifications_enabled:
            await self.repository.commit()
            return ScanReminderResponse(should_notify=False, confidence=confidence)

        zone = timezone(timedelta(hours=9)) if settings.timezone == "Asia/Seoul" else timezone.utc
        local_now = (now or datetime.now(timezone.utc)).astimezone(zone)
        if local_now.hour < settings.reminder_hour:
            await self.repository.commit()
            return ScanReminderResponse(should_notify=False, confidence=confidence)

        local_start = datetime.combine(local_now.date(), time.min, tzinfo=zone)
        local_end = local_start + timedelta(days=1)
        utc_start = local_start.astimezone(timezone.utc).replace(tzinfo=None)
        utc_end = local_end.astimezone(timezone.utc).replace(tzinfo=None)
        if await self.repository.has_completed_scan(user_id, utc_start, utc_end):
            await self.repository.commit()
            return ScanReminderResponse(should_notify=False, confidence=confidence)

        notification = await self.repository.daily_reminder(user_id, utc_start, utc_end)
        if notification is not None:
            await self.repository.commit()
            return ScanReminderResponse(should_notify=False, confidence=confidence)
        notification = await self.repository.add_reminder(user_id, confidence)
        await self.repository.commit()
        return ScanReminderResponse(
            should_notify=True,
            notification_id=notification.notification_id,
            title=notification.title,
            content=notification.content,
            confidence=confidence,
        )

    @staticmethod
    def _response(settings) -> UserSettingsResponse:
        return UserSettingsResponse(
            dark_mode=settings.dark_mode,
            language=settings.language,
            notifications_enabled=settings.notifications_enabled,
            reminder_hour=settings.reminder_hour,
            timezone=settings.timezone,
        )
