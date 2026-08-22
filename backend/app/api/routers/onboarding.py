from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.dependencies import get_current_user, get_archive_service
from app.services.archive_service import ArchiveService

from app.models.user import User

from app.repositories.question_repository import QuestionRepository
from app.repositories.scan_repository import ScanRepository

from app.schemas.question import QuestionSetResponse
from app.schemas.scan import StartOnboardingResponse

from app.services.onboarding_service import OnboardingService
from app.schemas.answer import (
    SubmitAnswersRequest,
)
from app.repositories.answer_repository import AnswerRepository

from app.repositories.pattern_repository import PatternRepository
from app.repositories.feature_repository import FeatureRepository
from app.repositories.growth_repository import GrowthRepository

from app.services.pattern_analysis_service import (
    PatternAnalysisService,
)

from app.schemas.pattern_analysis import (
    PatternAnalysisResponse,
)
from app.services.growth_service import GrowthService
from app.services.identity_service import IdentityService
from app.services.seed_initialization_service import (
    SeedInitializationService,
)

router = APIRouter(
    tags=["Onboarding"],
)

@router.get(
    "/questions",
    response_model=QuestionSetResponse,
    summary="온보딩 질문 조회",
    description="Seed Onboarding 질문 목록을 조회합니다.",
)
async def get_onboarding_questions(
    db: AsyncSession = Depends(get_db),
):
    """
    Seed Onboarding 질문 조회

    Flutter에서는 이 API 하나만 호출하면

    - Question Set
    - Questions
    - Question Options

    을 모두 받아 화면을 구성할 수 있다.
    """

    service = OnboardingService(
        question_repository=QuestionRepository(db),
        scan_repository=ScanRepository(db),
        answer_repository=None,
        pattern_analysis_service=None,
        growth_service=None,
    )

    return await service.get_onboarding_questions()


@router.post(
    "/start",
    response_model=StartOnboardingResponse,
    summary="온보딩 시작",
    description="새로운 온보딩 Scan을 시작하거나 진행 중인 Scan을 반환합니다.",
)
async def start_onboarding(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = OnboardingService(
        question_repository=QuestionRepository(db),
        scan_repository=ScanRepository(db),
        answer_repository=None,
        pattern_analysis_service=None,
        growth_service=None,
    )

    return await service.start_onboarding(current_user)


@router.post(
    "/answers",
    response_model=PatternAnalysisResponse,
    summary="온보딩 답변 저장",
    description="온보딩(Q1~Q6) 답변을 저장하고 Scan을 완료합니다.",
)
async def submit_answers(
    request: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    archive_service: ArchiveService = Depends(get_archive_service),
):
    answer_repository = AnswerRepository(db)
    pattern_repository = PatternRepository(db)
    growth_repository = GrowthRepository(db)

    service = OnboardingService(
        question_repository=QuestionRepository(db),
        scan_repository=ScanRepository(db),
        answer_repository=answer_repository,
        pattern_analysis_service=PatternAnalysisService(
            answer_repository=answer_repository,
            pattern_repository=pattern_repository,
            feature_repository=FeatureRepository(db),
        ),
        growth_service=GrowthService(
            growth_repository=growth_repository,
            pattern_repository=pattern_repository,
        ),
        identity_service=IdentityService(db),
        seed_initialization_service=SeedInitializationService(db),
    )

    response = await service.submit_answers(
        current_user=current_user,
        request=request,
    )

    await archive_service.record_onboarding_workflow(
        user_id=current_user.user_id,
        scan_id=request.scan_id,
        response=response,
    )

    return response

"""
@router.post(
    "/complete",
    response_model=PatternAnalysisResponse,
    summary="온보딩 완료",
    description="온보딩 답변을 기반으로 Seed를 생성합니다.",
)
async def complete_onboarding(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    service = PatternAnalysisService(

        answer_repository=AnswerRepository(db),

        pattern_repository=PatternRepository(db),

        feature_repository=FeatureRepository(db),

    )

    result = await service.analyze(
        scan_id=scan_id,
    )

    return PatternAnalysisResponse(

        pattern_id=result.metadata["pattern_id"],

        confidence=result.confidence_score,

        scores=result.scores,

        patterns=result.patterns,

        metadata=result.metadata,
    )"""
