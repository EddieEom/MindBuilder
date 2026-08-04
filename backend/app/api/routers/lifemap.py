from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.schemas.lifemap import (
    LifeMapResponse,
)

from app.services.feature_service import FeatureService
from app.services.pattern_service import PatternService
from app.services.identity_service import IdentityService
from app.services.growth_service import GrowthService
from app.services.life_map_service import LifeMapService

router = APIRouter(
    prefix="/lifemap",
    tags=["Life Map"],
)


# ======================================================
# Generate LifeMap
# ======================================================

@router.post(
    "",
    response_model=LifeMapResponse,
    summary="LifeMap 생성",
    description="현재 사용자의 Pattern, Identity, Growth 데이터를 기반으로 LifeMap을 생성합니다.",
)
async def generate_life_map(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    feature_service = FeatureService(db)

    pattern_service = PatternService(db)

    identity_service = IdentityService(db)

    growth_service = GrowthService(db)

    life_map_service = LifeMapService(db)

    feature_result = await feature_service.get_current_feature(
        current_user.user_id,
    )

    pattern_result = await pattern_service.get_current_pattern(
        current_user.user_id,
    )

    identity_result = await identity_service.get_current_identity(
        current_user.user_id,
    )

    growth_result = await growth_service.get_current_growth(
        current_user.user_id,
    )

    return await life_map_service.analyze(

        user_id=current_user.user_id,

        feature_result=feature_result,

        pattern_result=pattern_result,

        identity_result=identity_result,

        growth_result=growth_result,

    )


# ======================================================
# Current LifeMap
# ======================================================

@router.get(
    "",
    response_model=LifeMapResponse,
    summary="현재 LifeMap 조회",
    description="현재 저장된 LifeMap을 조회합니다.",
)
async def get_current_life_map(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = LifeMapService(db)

    return await service.get_current(

        user_id=current_user.user_id,

    )