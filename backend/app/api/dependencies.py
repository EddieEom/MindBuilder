from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token

from app.repositories.user_repository import UserRepository
from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.growth_repository import GrowthRepository
from app.repositories.pattern_repository import PatternRepository
from app.repositories.identity_repository import IdentityRepository
from app.repositories.life_map_repository import LifeMapRepository

from app.services.archive_service import ArchiveService
from app.services.dashboard_service import DashboardService
from app.services.growth_service import GrowthService

from app.ai.llm.client import LLMClient
from app.ai.recommendation.engine import RecommendationEngine
from app.ai.recommendation.repository import RecommendationRepository
from app.ai.recommendation.service import RecommendationService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# ==========================================================
# Authentication
# ==========================================================

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

    user = await repository.get_by_id(
        int(user_id)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="존재하지 않는 사용자입니다.",
        )

    return user


# ==========================================================
# Archive
# ==========================================================

def get_archive_service(
    db: AsyncSession = Depends(get_db),
) -> ArchiveService:

    from app.services.archive_service import ArchiveService

    return ArchiveService(
        db=db
    )


# ==========================================================
# Dashboard
# ==========================================================

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


# ==========================================================
# Growth
# ==========================================================

def get_growth_service(
    db: AsyncSession = Depends(get_db),
) -> GrowthService:

    return GrowthService(
        growth_repository=GrowthRepository(db),
        pattern_repository=PatternRepository(db),
    )


# ==========================================================
# LLM
# ==========================================================

def get_llm_client() -> LLMClient:

    return LLMClient()


# ==========================================================
# Recommendation
# ==========================================================

def get_recommendation_service(
    db: AsyncSession = Depends(get_db),
    llm_client: LLMClient = Depends(
        get_llm_client
    ),
) -> RecommendationService:

    recommendation_repository = (
        RecommendationRepository(db)
    )

    pattern_repository = (
        PatternRepository(db)
    )

    growth_repository = (
        GrowthRepository(db)
    )

    identity_repository = (
        IdentityRepository(db)
    )

    life_map_repository = (
        LifeMapRepository(db)
    )

    recommendation_engine = (
        RecommendationEngine(
            llm=llm_client
        )
    )

    return RecommendationService(
        engine=recommendation_engine,
        repository=recommendation_repository,
        pattern_repository=pattern_repository,
        growth_repository=growth_repository,
        identity_repository=identity_repository,
        life_map_repository=life_map_repository,
    )