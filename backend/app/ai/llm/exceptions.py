"""
MindBuilder LLM Exceptions
"""


# ==========================================================
# Base
# ==========================================================

class LLMException(Exception):
    """LLM 최상위 예외"""
    pass


# ==========================================================
# Model
# ==========================================================

class ModelLoadError(LLMException):
    """모델 로드 실패"""
    pass


# ==========================================================
# Provider
# ==========================================================

class ProviderError(LLMException):
    """Provider 호출 실패"""
    pass


# ==========================================================
# Inference
# ==========================================================

class InferenceError(LLMException):
    """LLM 추론 실패"""
    pass


# ==========================================================
# JSON
# ==========================================================

class InvalidJSONError(LLMException):
    """JSON Parsing 실패"""
    pass


class InvalidSchemaError(LLMException):
    """Schema Validation 실패"""
    pass


# ==========================================================
# Prompt
# ==========================================================

class PromptError(LLMException):
    """Prompt 생성 실패"""
    pass


# ==========================================================
# Retry
# ==========================================================

class RetryExceededError(LLMException):
    """Retry 횟수 초과"""
    pass


# ==========================================================
# Authentication
# ==========================================================

class AuthenticationError(LLMException):
    """API Key 오류"""
    pass


class RateLimitError(LLMException):
    """API Rate Limit"""
    pass


# ==========================================================
# Generation
# ==========================================================

class GenerationError(LLMException):
    """최종 생성 실패"""
    pass