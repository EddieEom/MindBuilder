#데이터 검증을 담당. 이메일 형식이 맞는지, 닉네임 길이는 적절한지 등을 Pydantic이 자동으로 체크.

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 1. 토큰 응답 모델
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# 2. 회원가입/로그인 요청 모델
class UserCreate(BaseModel):
    email: EmailStr
    nickname: str = Field(..., min_length=2, max_length=50)
    provider: str  # google, kakao 등
    provider_user_id: str
    profile_image: Optional[str] = None

# 3. 유저 정보 응답 모델
class UserRead(BaseModel):
    user_id: int
    email: EmailStr
    nickname: str
    profile_image: Optional[str] = None
    status: str

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic으로 변환하기 위함