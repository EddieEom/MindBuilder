from fastapi import FastAPI
from app.core.config import settings

# 라우터 임포트
from app.features.auth.router import router as auth_router

# FastAPI 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# 라우터 등록
app.include_router(auth_router)

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "environment": "development"
    }