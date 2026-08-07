from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.services.identity_service import (
    IdentityService,
)

from app.schemas.identity import (
    IdentityResponse,
)

from app.schemas.identity_history import (
    IdentityHistoryResponse,
)

router = APIRouter(
    prefix="/identity",
    tags=["Identity"],
)


# ======================================================
# Health
# ======================================================

@router.get(
    "/health",
    summary="Identity Engine 상태 확인",
)
async def health():

    return {

        "engine": "Identity Engine",

        "status": "ready",

    }


# ======================================================
# Current Identity
# ======================================================

@router.get(
    "/current",
    response_model=IdentityResponse,
)
async def get_current_identity(

    current_user: User = Depends(get_current_user),

    db: AsyncSession = Depends(get_db),

):

    service = IdentityService(db)

    return await service.get_current_identity(
        current_user.user_id
    )


@router.get(
    "/detail/{identity_id}",
    response_model=IdentityResponse,
)
async def get_identity_detail(

    identity_id: int,

    db: AsyncSession = Depends(get_db),

):

    service = IdentityService(db)

    return await service.get_detail(
        identity_id
    )


@router.get(
    "/history",
    response_model=IdentityHistoryResponse,
)
async def get_identity_history(

    current_user: User = Depends(get_current_user),

    db: AsyncSession = Depends(get_db),

):

    service = IdentityService(db)

    return await service.get_history(
        current_user.user_id
    )