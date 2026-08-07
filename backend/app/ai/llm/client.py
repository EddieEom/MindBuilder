import time
from typing import Type

from pydantic import (
    BaseModel,
    ValidationError,
)

from app.ai.llm.config import (
    DEFAULT_PROFILE,
    MODEL_NAME,
)

from app.ai.llm.exceptions import (
    InvalidSchemaError,
)

from app.ai.llm.parser import LLMParser

from app.ai.llm.providers.base import BaseLLMProvider
from app.ai.llm.providers.openrouter import OpenRouterProvider

from app.ai.llm.retry import RetryPolicy

from app.ai.llm.types import (
    GenerationMetadata,
    LLMResponse,
)

class LLMClient:

    def __init__(

        self,

        provider: BaseLLMProvider | None = None,

    ) -> None:

        self._provider = provider or OpenRouterProvider()

    async def generate(

        self,

        *,

        system: str,

        user: str,

        schema: Type[BaseModel],

        profile: str = DEFAULT_PROFILE,

    ) -> LLMResponse:

        start = time.perf_counter()

        async def task() -> str:

            return await self._provider.generate(

                system=system,

                user=user,

                profile=profile,

            )

        raw_text = await RetryPolicy.execute(task)

        parsed = LLMParser.parse(raw_text)

        try:

            validated = schema.model_validate(parsed)

        except ValidationError as e:

            raise InvalidSchemaError(
                str(e)
            ) from e

        latency = time.perf_counter() - start

        return LLMResponse(

            raw_text=raw_text,

            parsed=parsed,

            validated=validated,

            metadata=GenerationMetadata(

                model=MODEL_NAME,

                latency=latency,

                retry_count=1,

                success=True,

            ),

            usage=None,

        )