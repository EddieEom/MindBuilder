from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.features.auth.dependencies import get_current_user
from app.models.user import User
from .repository import SettingsRepository
from .schemas import ScanReminderResponse, UserSettingsResponse, UserSettingsUpdate
from .service import SettingsService

router = APIRouter(prefix="/settings", tags=["settings"])


def service(db: AsyncSession) -> SettingsService:
    return SettingsService(SettingsRepository(db))


@router.get("", response_model=UserSettingsResponse)
async def get_settings(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service(db).get(current_user.user_id)


@router.patch("", response_model=UserSettingsResponse)
async def update_settings(payload: UserSettingsUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        return await service(db).update(current_user.user_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/scan-reminder/check", response_model=ScanReminderResponse)
async def check_scan_reminder(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await service(db).check_scan_reminder(current_user.user_id)
