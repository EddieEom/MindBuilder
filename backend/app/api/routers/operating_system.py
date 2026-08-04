from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_archive_service,
    get_current_user,
)

from app.services.archive_service import ArchiveService
from app.core.database import get_db
from app.models.user import User
from app.schemas.operating_system import OperatingSystemResponse
from app.services.operating_system_service import OperatingSystemService

router = APIRouter(
    prefix="/operating-system",
    tags=["OperatingSystem"],
)


@router.get(
    "/health",
    summary="Operating System 상태 확인",
)
async def health():
    return {
        "engine": "Operating System",
        "status": "ready",
    }


@router.post(
    "/generate",
    response_model=OperatingSystemResponse,
    summary="Operating System 생성 및 저장",
)
async def generate_operating_system(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    service = OperatingSystemService(db)

    try:
        response = await service.generate(
            current_user.user_id
        )

        await archive_service.record_operating_system_workflow(
            user_id=current_user.user_id,
            os_id=response.os_id,
        )

        return response

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/current",
    response_model=OperatingSystemResponse,
    summary="현재 Operating System 조회",
)
async def get_current_operating_system(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OperatingSystemService(db)

    try:
        return await service.get_current(current_user.user_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get(
    "/history",
    response_model=list[OperatingSystemResponse],
    summary="Operating System 히스토리 조회",
)
async def get_operating_system_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OperatingSystemService(db)
    return await service.get_history(current_user.user_id)
