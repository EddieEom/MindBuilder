from fastapi import APIRouter, Depends, Query
from datetime import date
from app.api.dependencies import (
    get_archive_service,
    get_current_user,
)
from app.models.user import User
from app.schemas.archive import (
    ArchiveEventResponse,
    ArchiveListResponse,
)
from app.services.archive_service import ArchiveService

router = APIRouter(
    prefix="/archive",
    tags=["Archive"],
)


def _to_archive_response(event) -> ArchiveEventResponse:
    return ArchiveEventResponse(
        event_id=event.event_id,
        user_id=event.user_id,
        event_type=event.event_type,
        reference_id=event.reference_id,
        title=event.title,
        summary=event.summary,
        created_at=event.created_at,
    )


@router.get(
    "/recent",
    response_model=ArchiveListResponse,
    summary="최근 Archive Timeline 조회",
)
async def get_recent_archive(
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    events = await archive_service.get_recent_archive(
        user_id=current_user.user_id,
        limit=limit,
    )

    return ArchiveListResponse(
        events=[
            _to_archive_response(event)
            for event in events
        ]
    )


@router.get(
    "/type/{event_type}",
    response_model=ArchiveListResponse,
    summary="Archive 타입별 조회",
)
async def get_archive_by_type(
    event_type: str,
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    events = await archive_service.get_archive_by_type(
        user_id=current_user.user_id,
        event_type=event_type.upper(),
        limit=limit,
    )

    return ArchiveListResponse(
        events=[
            _to_archive_response(event)
            for event in events
        ]
    )


@router.get(
    "/calendar",
    response_model=ArchiveListResponse,
    summary="Archive 날짜별 조회",
)
async def get_archive_calendar(
    date: date,
    current_user: User = Depends(get_current_user),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    events = await archive_service.get_archive_calendar(
        user_id=current_user.user_id,
        date=date,
    )

    return ArchiveListResponse(
        events=[
            _to_archive_response(event)
            for event in events
        ]
    )


@router.get(
    "/timeline",
    response_model=ArchiveListResponse,
    summary="Growth Timeline 조회",
)
async def get_growth_timeline(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    events = await archive_service.get_growth_timeline(
        user_id=current_user.user_id,
        limit=limit,
    )

    return ArchiveListResponse(
        events=[
            _to_archive_response(event)
            for event in events
        ]
    )