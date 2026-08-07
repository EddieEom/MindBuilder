import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

from app.ai.llm.config import (
    MAX_RETRY,
    RETRY_DELAY,
)

from app.ai.llm.exceptions import (
    RetryExceededError,
)

T = TypeVar("T")


class RetryPolicy:

    @staticmethod
    async def execute(

        task: Callable[[], Awaitable[T]],

        *,

        max_retry: int = MAX_RETRY,

        delay: int = RETRY_DELAY,

    ) -> T:

        last_exception: Exception | None = None

        for attempt in range(1, max_retry + 1):

            try:

                return await task()

            except Exception as e:

                last_exception = e

                print(
                    f"[LLM Retry {attempt}/{max_retry}] {e}"
                )

                if attempt < max_retry:

                    await asyncio.sleep(delay)

        raise RetryExceededError(
            f"LLM failed after {max_retry} retries."
        ) from last_exception