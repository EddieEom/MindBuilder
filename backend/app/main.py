from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# 라우터 임포트
from app.features.auth.router import router as auth_router
from app.features.settings.router import router as settings_router
from app.api.routers import onboarding, growth, identity, lifemap, pattern, operating_system, archive, dashboard, recommendation
# FastAPI 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(
    onboarding.router,
    prefix="/api/v1/onboarding",
)
app.include_router(
    growth.router,
    prefix="/api/v1",
)
app.include_router(
    identity.router,
    prefix="/api/v1",
)
    
app.include_router(
    lifemap.router,
    prefix="/api/v1/lifemap",
)
app.include_router(
    pattern.router,
    prefix="/api/v1/pattern",
)
app.include_router(
    operating_system.router,
    prefix="/api/v1",
)
app.include_router(
    archive.router,
    prefix="/api/v1",
)

app.include_router(
    dashboard.router,
    prefix="/api/v1",
)

app.include_router(
    recommendation.router,
    prefix="/api/v1",
)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": "development"
    }
