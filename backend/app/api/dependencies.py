from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.services.archive_service import ArchiveService
from app.repositories.dashboard_repository import DashboardRepository
from app.services.dashboard_service import DashboardService
from app.services.growth_service import GrowthService
from app.repositories.growth_repository import GrowthRepository
from app.repositories.pattern_repository import PatternRepository
from app.ai.llm.client import LLMClient
from app.ai.recommendation.engine import RecommendationEngine
from app.ai.recommendation.repository import RecommendationRepository
from app.ai.recommendation.service import RecommendationService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
        )

    repository = UserRepository(db)

    user = await repository.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="존재하지 않는 사용자입니다.",
        )

    return user


def get_archive_service(
    db: AsyncSession = Depends(get_db),
) -> ArchiveService:
    from app.services.archive_service import ArchiveService
    return ArchiveService(db=db)


def get_dashboard_repository(
    db: AsyncSession = Depends(get_db),
) -> DashboardRepository:
    return DashboardRepository(db)


def get_dashboard_service(
    dashboard_repository: DashboardRepository = Depends(
        get_dashboard_repository
    ),
) -> DashboardService:
    return DashboardService(
        dashboard_repository=dashboard_repository,
    )

def get_growth_service(
    db: AsyncSession = Depends(get_db),
) -> GrowthService:

    return GrowthService(
        growth_repository=GrowthRepository(db),
        pattern_repository=PatternRepository(db),
    )


def get_llm_client() -> LLMClient:
    from app.ai.llm.client import LLMClient
    return LLMClient()


def get_recommendation_service(
    db: AsyncSession = Depends(get_db),
) -> RecommendationService:
    repository = RecommendationRepository(db)
    engine = RecommendationEngine(
        llm=LLMClient(),
    )

    return RecommendationService(
        engine=engine,
        repository=repository,
    )
