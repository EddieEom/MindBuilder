from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.services.identity_service import (
    IdentityService,
)

from app.schemas.identity import (
    IdentityResponse,
    IdentityFeedbackRequest,
    IdentityFeedbackResponse,
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
    current_user: User = Depends(get_current_user),

    db: AsyncSession = Depends(get_db),

):

    service = IdentityService(db)

    try:
        return await service.get_detail(identity_id, user_id=current_user.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


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


@router.post("/{identity_id}/feedback", response_model=IdentityFeedbackResponse)
async def submit_identity_feedback(
    identity_id: int,
    request: IdentityFeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await IdentityService(db).submit_feedback(identity_id, current_user.user_id, request)
    except ValueError as exc:
        message = str(exc)
        raise HTTPException(status_code=404 if message == "Identity not found." else 422, detail=message)
