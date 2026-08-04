from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models.system import ArchiveEvent


class ArchiveRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create_event(
        self,
        user_id: int,
        event_type: str,
        reference_id: int,
        title: str,
        summary: str | None = None,
    ) -> ArchiveEvent:
        event = ArchiveEvent(
            user_id=user_id,
            event_type=event_type,
            reference_id=reference_id,
            title=title,
            summary=summary,
        )
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def get_recent_events(
        self,
        user_id: int,
        limit: int = 30,
    ) -> list[ArchiveEvent]:
        stmt = (
            select(ArchiveEvent)
            .where(ArchiveEvent.user_id == user_id)
            .order_by(ArchiveEvent.created_at.desc(), ArchiveEvent.event_id.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_event(
        self,
        event_id: int,
    ) -> ArchiveEvent | None:
        stmt = select(ArchiveEvent).where(ArchiveEvent.event_id == event_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_events_by_type(
        self,
        user_id: int,
        event_type: str,
        limit: int = 50,
    ) -> list[ArchiveEvent]:
        stmt = (
            select(ArchiveEvent)
            .where(
                ArchiveEvent.user_id == user_id,
                ArchiveEvent.event_type == event_type,
            )
            .order_by(ArchiveEvent.created_at.desc(), ArchiveEvent.event_id.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_events_by_date(
        self,
        user_id: int,
        date: date,
    ) -> list[ArchiveEvent]:
        stmt = (
            select(ArchiveEvent)
            .where(
                ArchiveEvent.user_id == user_id,
                func.date(ArchiveEvent.created_at) == date,
            )
            .order_by(ArchiveEvent.created_at.desc(), ArchiveEvent.event_id.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def count_events(
        self,
        user_id: int,
    ) -> int:
        stmt = select(ArchiveEvent).where(ArchiveEvent.user_id == user_id)
        result = await self.db.execute(stmt)
        return len(result.scalars().all())

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

