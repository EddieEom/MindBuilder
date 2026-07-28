from fastapi import FastAPI
from app.core.config import settings

# 라우터 임포트
from app.features.auth.router import router as auth_router
from app.api.routers import onboarding, growth
# FastAPI 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(
    onboarding.router,
    prefix="/api/v1/onboarding",
)
app.include_router(
    growth.router,
    prefix="/api/v1",
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": "development"
    }