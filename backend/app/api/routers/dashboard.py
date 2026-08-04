from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_current_user,
    get_dashboard_service,
)

from app.models.user import User

from app.schemas.dashboard import DashboardResponse

from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
    summary="Dashboard 조회",
)
async def get_dashboard(

    current_user: User = Depends(
        get_current_user
    ),

    dashboard_service: DashboardService = Depends(
        get_dashboard_service
    ),

):

    return await dashboard_service.get_dashboard(
        current_user.user_id
    )