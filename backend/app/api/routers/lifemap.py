from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_archive_service,
    get_current_user,
)
from app.core.database import get_db

from app.models.user import User

from app.schemas.lifemap import (
    LifeMapResponse,
)

from app.services.life_map_service import LifeMapService
from app.services.archive_service import ArchiveService

router = APIRouter(
    tags=["Life Map"],
)


# ======================================================
# Generate LifeMap
# ======================================================

@router.post(
    "/generate",
    response_model=LifeMapResponse,
)
async def generate_life_map(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    archive_service: ArchiveService = Depends(get_archive_service),
):

    service = LifeMapService(db)

    response = await service.analyze(
        user_id=current_user.user_id,
    )

    # Archive 기록
    await archive_service.record_lifemap_workflow(
        user_id=current_user.user_id,
        life_map_id=response.metadata["life_map_id"],
    )

    return response


# ======================================================
# Current LifeMap
# ======================================================

@router.get(
    "",
    response_model=LifeMapResponse,
)
async def get_current_life_map(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = LifeMapService(db)

    return await service.get_current(
        user_id=current_user.user_id,
    )