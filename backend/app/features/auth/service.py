# backend/app/features/auth/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, OAuthAccount
from app.features.auth.schemas import UserCreate, Token
from app.core.security import create_access_token
from datetime import timedelta

class AuthService:
    async def get_or_create_user(self, db: AsyncSession, user_data: UserCreate) -> User:
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

            return user

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
        return new_user

    async def login_or_signup(self, db: AsyncSession, user_data: UserCreate) -> Token:
        # 1. 유저 확보
        user = await self.get_or_create_user(db, user_data)
        
        # 2. JWT 토큰 발급 (액세스 토큰)
        access_token = create_access_token(
            data={"sub": str(user.user_id), "email": user.email}
        )
        
        # 3. 리프레시 토큰 (나중에 DB 저장 로직 추가 예정)
        refresh_token = "refresh_token_placeholder" 
        
        return Token(access_token=access_token, refresh_token=refresh_token)

auth_service = AuthService()
