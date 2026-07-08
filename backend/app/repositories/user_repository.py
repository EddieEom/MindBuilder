from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


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