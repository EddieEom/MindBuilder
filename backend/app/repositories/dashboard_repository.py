from app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.operating_system import OperatingSystem
from app.models.analysis import (
    DataConfidence,
    PatternAnalysis,
    Insight,
)
from app.models.growth import NextAction
from app.models.scan import Scan
from app.models.system import ArchiveEvent

class DashboardRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_user(
        self,
        user_id: int,
    ) -> User | None:
        stmt = (
            select(User)
            .where(
                User.user_id == user_id
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # Human OS
    # =====================================================

    async def get_current_os(
        self,
        user_id: int,
    ) -> OperatingSystem | None:

        stmt = (
            select(OperatingSystem)
            .where(
                OperatingSystem.user_id == user_id,
                OperatingSystem.is_current.is_(True),
            )
            .order_by(
                OperatingSystem.generated_at.desc()
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # Data Confidence
    # =====================================================

    async def get_data_confidence(
        self,
        user_id: int,
    ) -> DataConfidence | None:

        stmt = (
            select(DataConfidence)
            .where(
                DataConfidence.user_id == user_id
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # Today's Insight
    # =====================================================

    async def get_latest_insight(
        self,
        user_id: int,
    ) -> Insight | None:

        stmt = (
            select(Insight)
            .join(
                PatternAnalysis,
                Insight.pattern_id == PatternAnalysis.pattern_id,
            )
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
            .order_by(
                Insight.created_at.desc()
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # Next Action
    # =====================================================

    async def get_next_action(
        self,
        user_id: int,
    ) -> NextAction | None:

        stmt = (
            select(NextAction)
            .where(
                NextAction.user_id == user_id,
                NextAction.status == "WAITING",
            )
            .order_by(
                NextAction.created_at.desc()
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    # =====================================================
    # Latest Pattern
    # =====================================================

    async def get_latest_pattern(
        self,
        user_id: int,
    ) -> PatternAnalysis | None:

        stmt = (
            select(PatternAnalysis)
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
            .order_by(
                PatternAnalysis.created_at.desc()
            )
            .limit(1)
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_recent_patterns(
        self,
        user_id: int,
        limit: int = 2,
    ) -> list[PatternAnalysis]:

        stmt = (
            select(PatternAnalysis)
            .join(
                Scan,
                PatternAnalysis.scan_id == Scan.scan_id,
            )
            .where(
                Scan.user_id == user_id
            )
            .order_by(
                PatternAnalysis.created_at.desc(),
                PatternAnalysis.pattern_id.desc(),
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    # =====================================================
    # Recent Archives
    # =====================================================

    async def get_recent_archives(
        self,
        user_id: int,
        limit: int = 5,
    ):

        stmt = (
            select(ArchiveEvent)
            .where(
                ArchiveEvent.user_id == user_id
            )
            .order_by(
                ArchiveEvent.created_at.desc()
            )
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return result.scalars().all()
