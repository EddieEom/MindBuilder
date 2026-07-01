# backend/app/features/auth/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.features.auth import schemas
from app.features.auth.service import auth_service
from app.features.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/oauth", response_model=schemas.Token)
async def oauth_login(
    user_data: schemas.UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 서비스 로직 호출 (토큰 반환)
    return await auth_service.login_or_signup(db, user_data)