from sqlalchemy import (
    select,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.models.identity import (
    Identity,
    IdentityKeyword,
    IdentityKeywordMap,
    IdentityStrength,
    IdentityGrowthPoint,
)


class IdentityRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

    # ==========================================================
    # Identity
    # ==========================================================

    async def create(
        self,
        identity: Identity,
    ):

        self.db.add(identity)

        await self.db.flush()

        await self.db.refresh(identity)

        return identity

    async def get_by_id(
        self,
        identity_id: int,
    ) -> Identity | None:
        stmt = select(Identity).where(
            Identity.identity_id == identity_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_current(
        self,
        user_id: int,
    ) -> Identity | None:

        stmt = (

            select(Identity)

            .where(

                Identity.user_id == user_id,

                Identity.is_current.is_(True),

            )

        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # ==========================================================
    # Keyword
    # ==========================================================

    async def create_keyword(
        self,
        identity_id: int,
        keyword_name: str,
        weight: float = 1.0,
    ):

        # Keyword 조회
        stmt = (
            select(IdentityKeyword)
            .where(
                IdentityKeyword.keyword_name == keyword_name
            )
        )

        result = await self.db.execute(stmt)

        keyword = result.scalar_one_or_none()

        # 없으면 생성
        if keyword is None:

            keyword = IdentityKeyword(

                keyword_name=keyword_name,

                category=None,

            )

            self.db.add(keyword)

            await self.db.flush()

        # 이미 Mapping이 있는지 확인
        stmt = (
            select(IdentityKeywordMap)
            .where(
                IdentityKeywordMap.identity_id == identity_id,
                IdentityKeywordMap.keyword_id == keyword.keyword_id,
            )
        )

        result = await self.db.execute(stmt)

        mapping = result.scalar_one_or_none()

        if mapping is None:

            self.db.add(

                IdentityKeywordMap(

                    identity_id=identity_id,

                    keyword_id=keyword.keyword_id,

                    weight=weight,

                )

            )

    async def get_keywords(
        self,
        identity_id: int,
    ) -> list[str]:

        stmt = (

            select(
                IdentityKeyword.keyword_name
            )

            .join(
                IdentityKeywordMap,
                IdentityKeyword.keyword_id
                ==
                IdentityKeywordMap.keyword_id
            )

            .where(
                IdentityKeywordMap.identity_id
                ==
                identity_id
            )

        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    # ==========================================================
    # Strength
    # ==========================================================

    async def create_strength(
        self,
        identity_id: int,
        content: str,
        display_order: int,
    ):

        self.db.add(

            IdentityStrength(

                identity_id=identity_id,

                content=content,

                display_order=display_order,

            )

        )

    async def get_strengths(
        self,
        identity_id: int,
    ) -> list[str]:

        stmt = (

            select(
                IdentityStrength.content
            )

            .where(
                IdentityStrength.identity_id
                ==
                identity_id
            )

            .order_by(
                IdentityStrength.display_order
            )

        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    # ==========================================================
    # Growth Point
    # ==========================================================

    async def create_growth_point(
        self,
        identity_id: int,
        content: str,
        display_order: int,
    ):

        self.db.add(

            IdentityGrowthPoint(

                identity_id=identity_id,

                content=content,

                display_order=display_order,

            )

        )

    async def get_growth_points(
        self,
        identity_id: int,
    ) -> list[str]:

        stmt = (

            select(
                IdentityGrowthPoint.content
            )

            .where(
                IdentityGrowthPoint.identity_id
                ==
                identity_id
            )

            .order_by(
                IdentityGrowthPoint.display_order
            )

        )

        result = await self.db.execute(stmt)

        return list(
            result.scalars().all()
        )

    # ==========================================================
    # Transaction
    # ==========================================================

    async def commit(self):

        await self.db.commit()

    async def rollback(self):

        await self.db.rollback()