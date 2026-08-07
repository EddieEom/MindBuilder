# backend/app/features/auth/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.features.auth import schemas
from app.features.auth.service import auth_service
from app.features.auth.dependencies import get_current_user
from app.models.user import User
from app.features.auth.schemas import (
    UserProfileResponse,
    UpdateNicknameRequest,
    UpdateNicknameResponse,
    UpdateProfileImageResponse,
    UpdateProfileImageRequest,

)
from app.services.user_service import (
    UserService,
)

from app.repositories.user_repository import (
    UserRepository,
)

from app.repositories.identity_repository import (
    IdentityRepository,
)

from app.repositories.operating_system_repository import (
    OperatingSystemRepository,
)
from app.repositories.growth_repository import (
    GrowthRepository,
)

from app.repositories.life_map_repository import (
    LifeMapRepository,
)

from app.repositories.pattern_repository import (
    PatternRepository,
)

from app.repositories.archive_repository import (
    ArchiveRepository,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/oauth", response_model=schemas.Token)
async def oauth_login(
    user_data: schemas.UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 서비스 로직 호출 (토큰 반환)
    return await auth_service.login_or_signup(db, user_data)


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="내 프로필 조회",
)
async def get_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = UserService(
        user_repository=UserRepository(db),
        identity_repository=IdentityRepository(db),
        operating_system_repository=OperatingSystemRepository(db),

        growth_repository=GrowthRepository(db),
        life_map_repository=LifeMapRepository(db),
        pattern_repository=PatternRepository(db),
        archive_repository=ArchiveRepository(db),
    )

    return await service.get_me(
        current_user.user_id
    )


@router.patch(
    "/me",
    response_model=UpdateNicknameResponse,
    summary="닉네임 변경",
)
async def update_nickname(
    request: UpdateNicknameRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = UserService(
        user_repository=UserRepository(db),
        identity_repository=IdentityRepository(db),
        operating_system_repository=OperatingSystemRepository(db),

        growth_repository=GrowthRepository(db),
        life_map_repository=LifeMapRepository(db),
        pattern_repository=PatternRepository(db),
        archive_repository=ArchiveRepository(db),
    )

    return await service.update_nickname(
        current_user.user_id,
        request.nickname
    )


@router.patch(
    "/profile-image",
    response_model=UpdateProfileImageResponse,
    summary="프로필 이미지 변경",
)
async def update_profile_image(
    request: UpdateProfileImageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    
    service = UserService(
        user_repository=UserRepository(db),
        identity_repository=IdentityRepository(db),
        operating_system_repository=OperatingSystemRepository(db),

        growth_repository=GrowthRepository(db),
        life_map_repository=LifeMapRepository(db),
        pattern_repository=PatternRepository(db),
        archive_repository=ArchiveRepository(db),
    )


    return await service.update_profile_image(
        current_user.user_id,
        request.profile_image,
    )



@router.get("/export")
async def export_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    print("ROUTER EXPORT START")
    service = UserService(
        user_repository=UserRepository(db),
        identity_repository=IdentityRepository(db),
        operating_system_repository=OperatingSystemRepository(db),

        growth_repository=GrowthRepository(db),
        life_map_repository=LifeMapRepository(db),
        pattern_repository=PatternRepository(db),
        archive_repository=ArchiveRepository(db),
    )

    return await service.export_data(
        current_user.user_id
    )


@router.delete(
    "/me",
    summary="회원탈퇴",
)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = UserService(
        user_repository=UserRepository(db),
        identity_repository=IdentityRepository(db),
        operating_system_repository=OperatingSystemRepository(db),
        growth_repository=GrowthRepository(db),
        life_map_repository=LifeMapRepository(db),
        pattern_repository=PatternRepository(db),
        archive_repository=ArchiveRepository(db),
    )

    return await service.delete_account(
        current_user.user_id
    )