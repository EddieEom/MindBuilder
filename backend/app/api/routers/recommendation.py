from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.api.dependencies import (
    get_current_user,
    get_recommendation_service,
)

from app.models.user import User

from app.ai.recommendation.service import (
    RecommendationService,
)

from app.schemas.recommendation import (
    RecommendationGenerateResponse,
    RecommendationCurrentResponse,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendation"],
)


@router.get(
    "/health",
    summary="Recommendation Engine 상태 확인",
)
async def health():

    return {
        "engine": "Recommendation Engine",
        "status": "ready",
    }


@router.post(
    "/generate",
    response_model=RecommendationGenerateResponse,
    summary="현재 분석 결과 기반 Recommendation 생성",
)
async def generate_recommendation(

    current_user: User = Depends(
        get_current_user
    ),

    recommendation_service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    try:

        return await recommendation_service.generate(
            current_user.user_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/current",
    response_model=RecommendationCurrentResponse,
    summary="현재 Recommendation 조회",
)
async def get_current_recommendation(

    current_user: User = Depends(
        get_current_user
    ),

    recommendation_service: RecommendationService = Depends(
        get_recommendation_service
    ),
):

    try:

        return await recommendation_service.get_current(
            current_user.user_id
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )