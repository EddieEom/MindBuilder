# backend/app/features/auth/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, OAuthAccount
from app.features.auth.schemas import UserCreate, Token
from app.features.auth.schemas import UserCreate, Token
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

class AuthService:
    async def get_or_create_user(self, db: AsyncSession, user_data: UserCreate) -> tuple[User, bool]:
        # 기존 로직: 유저 조회 또는 생성
        stmt = select(OAuthAccount).where(
            OAuthAccount.provider == user_data.provider,
            OAuthAccount.provider_user_id == user_data.provider_user_id
        )
        result = await db.execute(stmt)
        oauth_account = result.scalar_one_or_none()

        if oauth_account:
            user = await db.get(User, oauth_account.user_id)

            if user is None:
                raise ValueError("OAuth account user not found.")

            return user, False

        new_user = User(
            email=user_data.email,
            nickname=user_data.nickname,
            profile_image=user_data.profile_image,
            status="ACTIVE"
        )
        db.add(new_user)
        await db.flush()

        new_oauth = OAuthAccount(
            user_id=new_user.user_id,
            provider=user_data.provider,
            provider_user_id=user_data.provider_user_id,
            provider_email=user_data.email
        )
        db.add(new_oauth)
        await db.commit()
        await db.refresh(new_user)
        return new_user, True

    async def login_or_signup(self, db: AsyncSession, user_data: UserCreate) -> Token:
        # 1. 유저 확보
        user, is_new_user = await self.get_or_create_user(db, user_data)
        
        # 2. Access Token 발급
        access_token = create_access_token(
            data={
                "sub": str(user.user_id),
                "email": user.email,
            }
        )

        # 3. Refresh Token 발급
        refresh_token = create_refresh_token(
            data={
                "sub": str(user.user_id),
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            is_new_user=is_new_user,
        )

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> Token:
        user_id = decode_refresh_token(refresh_token)

        if user_id is None:
            raise ValueError("유효하지 않거나 만료된 Refresh Token입니다.")

        access_token = create_access_token(
            data={
                "sub": str(user_id),
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

auth_service = AuthService()
