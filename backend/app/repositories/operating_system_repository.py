from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.operating_system import (
    OperatingSystem,
    CoreValue,
    OSCoreValue,
)


class OperatingSystemRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # ======================================================
    # Core Value
    # ======================================================

    async def get_or_create_core_value(
        self,
        value_name: str,
        description: str | None = None,
    ) -> CoreValue:
        stmt = (
            select(CoreValue)
            .where(CoreValue.value_name == value_name)
        )

        result = await self.db.execute(stmt)
        core_value = result.scalar_one_or_none()

        if core_value is not None:
            return core_value

        core_value = CoreValue(
            value_name=value_name,
            description=description,
        )

        self.db.add(core_value)
        await self.db.flush()
        await self.db.refresh(core_value)

        return core_value

    async def create_os_core_value(
        self,
        operating_system_id: int,
        value_id: int,
        priority: int = 1,
    ) -> OSCoreValue:
        os_core_value = OSCoreValue(
            os_id=operating_system_id,
            value_id=value_id,
            priority=priority,
        )

        self.db.add(os_core_value)
        await self.db.flush()
        return os_core_value

    # ======================================================
    # Operating System
    # ======================================================

    async def create_operating_system(
        self,
        operating_system: OperatingSystem,
    ) -> OperatingSystem:
        self.db.add(operating_system)
        await self.db.flush()
        await self.db.refresh(operating_system)
        return operating_system

    async def get_by_id(
        self,
        os_id: int,
    ) -> OperatingSystem | None:
        stmt = select(OperatingSystem).where(
            OperatingSystem.os_id == os_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_current(
        self,
        user_id: int,
    ) -> OperatingSystem | None:
        stmt = (
            select(OperatingSystem)
            .where(
                OperatingSystem.user_id == user_id,
                OperatingSystem.is_current.is_(True),
            )
            .options(
                selectinload(OperatingSystem.identity),
                selectinload(OperatingSystem.life_map),
                selectinload(OperatingSystem.core_values).selectinload(
                    OSCoreValue.core_value
                ),
            )
            .order_by(
                OperatingSystem.generated_at.desc(),
                OperatingSystem.os_id.desc(),
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_history(
        self,
        user_id: int,
        limit: int = 30,
    ) -> list[OperatingSystem]:
        stmt = (
            select(OperatingSystem)
            .where(OperatingSystem.user_id == user_id)
            .options(
                selectinload(OperatingSystem.identity),
                selectinload(OperatingSystem.life_map),
                selectinload(OperatingSystem.core_values).selectinload(
                    OSCoreValue.core_value
                ),
            )
            .order_by(
                OperatingSystem.generated_at.desc(),
                OperatingSystem.os_id.desc(),
            )
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    # ======================================================
    # Transaction
    # ======================================================

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()
