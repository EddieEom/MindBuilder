from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis import DataConfidence
from app.models.scan import Scan
from app.models.system import Notification
from app.models.user import UserSettings


class SettingsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create(self, user_id: int) -> UserSettings:
        settings = await self.db.get(UserSettings, user_id)
        if settings is None:
            settings = UserSettings(user_id=user_id)
            self.db.add(settings)
            await self.db.flush()
        return settings

    async def has_completed_scan(self, user_id: int, start: datetime, end: datetime) -> bool:
        stmt = select(Scan.scan_id).where(
            Scan.user_id == user_id,
            Scan.status == "COMPLETED",
            Scan.completed_at >= start,
            Scan.completed_at < end,
        ).limit(1)
        return (await self.db.execute(stmt)).scalar_one_or_none() is not None

    async def confidence(self, user_id: int) -> int:
        stmt = select(DataConfidence.confidence_score).where(DataConfidence.user_id == user_id)
        score = (await self.db.execute(stmt)).scalar_one_or_none()
        return round(float(score or 0))

    async def daily_reminder(self, user_id: int, start: datetime, end: datetime) -> Notification | None:
        stmt = select(Notification).where(
            Notification.user_id == user_id,
            Notification.title == "오늘의 Mind Scan",
            Notification.created_at >= start,
            Notification.created_at < end,
        ).order_by(Notification.created_at.desc()).limit(1)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def add_reminder(self, user_id: int, confidence: int) -> Notification:
        notification = Notification(
            user_id=user_id,
            title="오늘의 Mind Scan",
            content=f"오늘도 메타인지를 해볼까요? 현재 당신의 데이터 신뢰도는 {confidence}%입니다.",
        )
        self.db.add(notification)
        await self.db.flush()
        await self.db.refresh(notification)
        return notification

    async def commit(self) -> None:
        await self.db.commit()
