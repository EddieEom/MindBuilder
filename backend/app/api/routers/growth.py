from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

from app.repositories.answer_repository import AnswerRepository
from app.repositories.pattern_repository import PatternRepository
from app.repositories.feature_repository import FeatureRepository
from app.repositories.growth_repository import GrowthRepository

from app.services.pattern_analysis_service import PatternAnalysisService
from app.services.growth_service import GrowthService

from app.models.growth import Feedback, NextAction
from app.api.dependencies import (
    get_current_user,
    get_growth_service,
)

from app.schemas.growth_current import GrowthCurrentResponse
from app.schemas.feedback import (
    FeedbackRequest,
    FeedbackResponse,
)

router = APIRouter(
    prefix="/growth",
    tags=["Growth"],
)


class AnalyzeRequest(BaseModel):
    scan_id: int


class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class NextActionCreate(BaseModel):
    recommendation_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None


@router.get(
    "/health",
    summary="Growth Engine 상태 확인",
)
async def health():
    return {
        "engine": "Growth Engine",
        "status": "ready",
    }


@router.post(
    "/analyze",
    summary="Scan 기반 Growth 분석 실행",
)
async def analyze_growth(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # 재사용 가능한 리포지토리/서비스 인스턴스 구성
    answer_repo = AnswerRepository(db)
    pattern_repo = PatternRepository(db)
    growth_repo = GrowthRepository(db)

    pattern_service = PatternAnalysisService(
        answer_repository=answer_repo,
        pattern_repository=pattern_repo,
        feature_repository=FeatureRepository(db),
    )

    growth_service = GrowthService(
        growth_repository=growth_repo,
        pattern_repository=pattern_repo,
    )

    # Pattern 분석 → Growth 분석
    feature_result = await pattern_service.analyze(request.scan_id)

    pattern_id = int(feature_result.metadata.get("pattern_id", 0))

    growth_response = await growth_service.analyze(
        user_id=current_user.user_id,
        feature_result=feature_result,
        pattern_id=pattern_id,
    )

    await growth_repo.commit()

    return growth_response




@router.get(
    "/current",
    response_model=GrowthCurrentResponse,
    summary="현재 Growth 조회",
)
async def get_current_growth(
    current_user: User = Depends(
        get_current_user
    ),
    growth_service: GrowthService = Depends(
        get_growth_service
    ),
):
    return await growth_service.get_current(
        current_user.user_id
    )



@router.get(
    "/{growth_analysis_id}",
    summary="저장된 Growth 분석 조회",
)
async def get_growth_analysis(
    growth_analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GrowthRepository(db)

    analysis = await repo.get_owned_analysis(growth_analysis_id, current_user.user_id)

    if analysis is None:
        raise HTTPException(status_code=404, detail="GrowthAnalysis not found")

    items = await repo.get_growth_items(analysis.growth_analysis_id)

    # 간단한 직렬화
    return {
        "growth_analysis": {
            "growth_analysis_id": analysis.growth_analysis_id,
            "pattern_id": analysis.pattern_id,
            "confidence": float(analysis.confidence or 0),
            "created_at": analysis.created_at,
        },
        "items": [
            {
                "growth_item_id": it.growth_item_id,
                "title": it.title,
                "content": it.content,
                "priority": it.priority,
            }
            for it in items
        ],
        "feedbacks": [
            {
                "rating": f.rating,
                "comment": f.comment,
                "created_at": f.created_at,
            }
            for f in await repo.get_feedbacks(analysis.growth_analysis_id)
        ],
    }


@router.post(
    "/{growth_analysis_id}/feedback",
    summary="Growth 분석에 대한 피드백 저장",
)
async def submit_feedback(
    growth_analysis_id: int,
    request: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GrowthRepository(db)

    if await repo.get_owned_analysis(growth_analysis_id, current_user.user_id) is None:
        raise HTTPException(status_code=404, detail="GrowthAnalysis not found")
    created = await repo.upsert_feedback(
        growth_analysis_id=growth_analysis_id, rating=request.rating, comment=request.comment,
    )

    await repo.commit()

    return {
        "feedback_id": created.feedback_id,
        "rating": created.rating,
        "comment": created.comment,
    }


@router.post(
    "/actions",
    summary="NextAction 생성 (추천 기반 다음 행동)",
)
async def create_next_action(
    request: NextActionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GrowthRepository(db)

    recommendation = await repo.get_owned_recommendation(request.recommendation_id, current_user.user_id)
    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    existing = await repo.get_actions(current_user.user_id, [request.recommendation_id])
    if existing:
        created = existing[0]
        return {"action_id": created.action_id, "status": created.status, "created_at": created.created_at}

    action = NextAction(
        user_id=int(current_user.user_id),
        recommendation_id=int(request.recommendation_id),
        title=request.title,
        description=request.description,
        status="WAITING",
    )

    created = await repo.create_next_action(action)

    await repo.commit()

    return {
        "action_id": created.action_id,
        "status": created.status,
        "created_at": created.created_at,
    }


