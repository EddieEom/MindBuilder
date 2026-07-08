from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan import Scan


class ScanRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_in_progress_scan(
        self,
        user_id: int,
        scan_type: str = "ONBOARDING",
    ) -> Scan | None:

        stmt = (
            select(Scan)
            .where(
                Scan.user_id == user_id,
                Scan.scan_type == scan_type,
                Scan.status == "IN_PROGRESS",
            )
            .limit(1)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_scan(
        self,
        user_id: int,
        scan_type: str = "ONBOARDING",
    ) -> Scan:

        scan = Scan(
            user_id=user_id,
            scan_type=scan_type,
            started_at=datetime.now(),
            status="IN_PROGRESS",
        )

        self.db.add(scan)

        await self.db.commit()
        await self.db.refresh(scan)

        return scan

    async def update_completed_scan(
        self,
        scan: Scan,
    ) -> None:
        """
        Scan 완료 처리
        """

        scan.status = "COMPLETED"
        scan.completed_at = datetime.now()


    async def get_by_id(
        self,
        scan_id: int,
    ) -> Scan | None:
        """
        Scan ID로 조회
        """

        stmt = (
            select(Scan)
            .where(Scan.scan_id == scan_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()