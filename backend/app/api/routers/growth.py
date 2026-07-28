from fastapi import APIRouter

router = APIRouter(
    prefix="/growth",
    tags=["Growth"],
)


@router.get(
    "/health",
    summary="Growth Engine 상태 확인",
)
async def health():

    return {
        "engine": "Growth Engine",
        "status": "ready",
    }


# ======================================================
# TODO
# ======================================================

"""
향후 구현 예정

GET    /growth/{growth_analysis_id}

    저장된 Growth 조회

POST   /growth/analyze

    Pattern 기반 Growth 재분석

POST   /growth/feedback

    Growth 결과 피드백 저장

GET    /growth/history

    과거 Growth 목록 조회
"""