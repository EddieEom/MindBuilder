from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import func, select

from app.models.scan import Scan
from app.models.analysis import PatternAnalysis
from app.models.system import ArchiveEvent
from app.models.growth import NextAction, GrowthAnalysis 
from app.models.user import OAuthAccount

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        stmt = (
            select(User)
            .where(User.user_id == user_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


    # ======================================================
    # OAuth
    # ======================================================

    async def get_provider(
        self,
        user_id: int,
    ) -> str | None:

        stmt = (
            select(OAuthAccount.provider)
            .where(
                OAuthAccount.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()


    # ======================================================
    # Counts
    # ======================================================

    async def get_scan_count(
        self,
        user_id: int,
    ) -> int:

        stmt = (
            select(func.count())
            .select_from(Scan)
            .where(
                Scan.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()


    async def get_pattern_count(
        self,
        user_id: int,
    ) -> int:

        stmt = (
            select(func.count())
            .select_from(PatternAnalysis)
            .join(PatternAnalysis.scan)
            .where(
                Scan.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()

    async def get_analysis_count(
            self,
            user_id: int,
        ) -> int:
    
            stmt = (
                select(func.count())
                .select_from(GrowthAnalysis)
                .join(
                    GrowthAnalysis.pattern_analysis,
                )
                .join(
                    PatternAnalysis.scan,
                )
                .where(
                    Scan.user_id == user_id
                )
            )
    
            result = await self.db.execute(stmt)
    
            return result.scalar_one()

    
    async def get_archive_count(
        self,
        user_id: int,
    ) -> int:

        stmt = (
            select(func.count())
            .select_from(ArchiveEvent)
            .where(
                ArchiveEvent.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()


    async def get_goal_count(
        self,
        user_id: int,
    ) -> int:

        stmt = (
            select(func.count())
            .select_from(NextAction)
            .where(
                NextAction.user_id == user_id
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()


    # ======================================================
    # Update
    # ======================================================

    async def update_nickname(
        self,
        user_id: int,
        nickname: str,
    ) -> User:

        user = await self.get_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        user.nickname = nickname

        await self.db.flush()

        await self.db.refresh(
            user
        )

        return user


    # ======================================================
    # Update Profile Image
    # ======================================================

    async def update_profile_image(
        self,
        user_id: int,
        profile_image: str,
    ) -> User:

        user = await self.get_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "User not found."
            )

        user.profile_image = profile_image

        await self.db.flush()

        await self.db.refresh(
            user
        )

        return user


    async def delete(
        self,
        user_id: int,
    ):

        user = await self.get_by_id(user_id)

        if user is None:
            return False

        await self.db.delete(user)

        return True
        
    # ======================================================
    # Transaction
    # ======================================================

    async def commit(
        self,
    ):

        await self.db.commit()


    async def rollback(
        self,
    ):

        await self.db.rollback()


    