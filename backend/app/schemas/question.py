from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class QuestionOptionResponse(BaseModel):
    """
    질문 보기(Response)

    Flutter에서 각 질문의 보기를 렌더링하기 위한 데이터
    """

    option_id: int
    option_text: str
    option_value: Optional[str] = None
    display_order: int
    is_other: bool

    model_config = ConfigDict(from_attributes=True)


class QuestionResponse(BaseModel):
    """
    질문(Response)

    질문 정보와 보기 목록을 함께 반환한다.
    """

    question_id: int
    question_code: str
    title: str
    description: Optional[str] = None
    question_type: str
    display_order: int
    options: List[QuestionOptionResponse]
    target_features: List[str] = Field(default_factory=list)
    information_need: float = 0.0
    selection_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionSetResponse(BaseModel):
    """
    질문 세트(Response)

    하나의 질문 세트(Seed Scan)에 포함된 모든 질문을 반환한다.
    """

    set_id: int
    set_name: str
    description: Optional[str] = None
    target_stage: str
    questions: List[QuestionResponse]
    adaptive: bool = False
    source_scan_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
