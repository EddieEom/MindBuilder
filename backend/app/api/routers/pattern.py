from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

from app.repositories.pattern_repository import PatternRepository
from app.repositories.answer_repository import AnswerRepository
from app.repositories.feature_repository import FeatureRepository
from app.services.pattern_analysis_service import PatternAnalysisService

router = APIRouter(
    prefix="/pattern",
    tags=["Pattern"],
)


class AnalyzeRequest(BaseModel):
    scan_id: int


@router.post(
    "/analyze",
    summary="Scan 기반 패턴 분석 실행",
)
async def analyze_pattern(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """지정한 `scan_id`에 대해 Feature 추출 및 Pattern 생성 후 결과를 반환합니다."""

    answer_repo = AnswerRepository(db)
    pattern_repo = PatternRepository(db)

    service = PatternAnalysisService(
        answer_repository=answer_repo,
        pattern_repository=pattern_repo,
        feature_repository=FeatureRepository(db),
    )

    result = await service.analyze(request.scan_id)

    return {
        "pattern_id": result.metadata.get("pattern_id"),
        "confidence": result.confidence_score,
        "scores": result.scores,
        "patterns": result.patterns,
        "metadata": result.metadata,
    }


@router.get(
    "/latest",
    summary="현재 사용자 최신 Pattern 조회",
)
async def get_latest_pattern(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PatternRepository(db)

    pattern = await repo.get_latest_pattern(current_user.user_id)

    if pattern is None:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return {
        "pattern_id": pattern.pattern_id,
        "confidence": float(pattern.confidence or 0),
        "scores": {
            "future": float(pattern.future_score or 0),
            "creativity": float(pattern.creativity_score or 0),
            "execution": float(pattern.execution_score or 0),
            "uncertainty": float(pattern.uncertainty_score or 0),
            "perfectionism": float(pattern.perfectionism_score or 0),
            "resilience": float(pattern.resilience_score or 0),
        },
        "created_at": pattern.created_at,
    }


@router.get(
    "/recent",
    summary="현재 사용자 최근 Pattern 목록 조회",
)
async def get_recent_patterns(
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PatternRepository(db)

    patterns = await repo.get_recent_patterns(
        user_id=current_user.user_id,
        limit=limit,
    )

    return [
        {
            "pattern_id": p.pattern_id,
            "created_at": p.created_at,
            "scores": {
                "future": float(p.future_score or 0),
                "creativity": float(p.creativity_score or 0),
                "execution": float(p.execution_score or 0),
            },
        }
        for p in patterns
    ]
