from pydantic import BaseModel, Field


class AnswerRequest(BaseModel):
    question_id: int = Field(..., description="질문 ID")
    option_id: int = Field(..., description="선택한 보기 ID")
    point_value: int = Field(
        default=0,
        description="Q1 포인트 (POINT 타입 질문에서 사용)",
    )
    detail_text: str | None = Field(
        default=None,
        description="기타 입력 내용",
    )


class SubmitAnswersRequest(BaseModel):
    scan_id: int = Field(..., description="진행 중인 Scan ID")
    answers: list[AnswerRequest]


class SubmitAnswersResponse(BaseModel):
    message: str
    completed: bool