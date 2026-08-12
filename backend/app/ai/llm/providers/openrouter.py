from openai.types.realtime import conversation_item_input_audio_transcription_failed_event
import time

from openai import (
    APIConnectionError,
    APIError,
    AsyncOpenAI,
    AuthenticationError as OpenAIAuthenticationError,
    RateLimitError as OpenAIRateLimitError,
)

from app.ai.llm.config import (
    LLM_PROFILES,
    MODEL_NAME,
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)

from app.ai.llm.exceptions import (
    AuthenticationError,
    InferenceError,
    ProviderError,
    RateLimitError,
)

from app.ai.llm.providers.base import BaseLLMProvider


class OpenRouterProvider(BaseLLMProvider):

    def __init__(self) -> None:

        self.client = AsyncOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            default_headers={
                "X-Title": "MindBuilder",
            },
        )

    async def generate(
        self,
        *,
        system: str,
        user: str,
        profile: str,
    ) -> str:

        if profile not in LLM_PROFILES:
            raise ValueError(
                f"Unknown profile : {profile}"
            )

        config = LLM_PROFILES[profile]

        try:

            response = await self.client.chat.completions.create(

                model=MODEL_NAME,

                messages=[
                    {
                        "role": "system",
                        "content": system,
                    },
                    {
                        "role": "user",
                        "content": user,
                    },
                ],

                temperature=config["temperature"],
                top_p=config["top_p"],
                max_tokens=config["max_tokens"],
            )

            # ==================================================
            # Response Diagnostics
            # ==================================================

            if not response.choices:
                raise InferenceError(
                    "LLM returned no choices."
                )

            choice = response.choices[0]

            message = choice.message

            finish_reason = getattr(
                choice,
                "finish_reason",
                None,
            )

            print("\n========== OPENROUTER RESPONSE DEBUG ==========")
            print("finish_reason:", finish_reason)
            print("model:", MODEL_NAME)
            print("profile:", profile)
            print("max_tokens:", config["max_tokens"])
            print("content_length:", len(message.content or ""))
            print("================================================\n")

            
            if message is None:
                raise InferenceError(
                    "LLM returned no message."
                )

            raw_text = message.content

            if raw_text is None or not raw_text.strip():

                finish_reason = getattr(
                    choice,
                    "finish_reason",
                    None,
                )

                reasoning_content = getattr(
                    message,
                    "reasoning_content",
                    None,
                )

                raise InferenceError(
                    "LLM returned empty content. "
                    f"finish_reason={finish_reason}, "
                    f"has_reasoning={bool(reasoning_content)}"
                )

            return raw_text

        except OpenAIAuthenticationError as e:

            raise AuthenticationError(
                str(e)
            ) from e

        except OpenAIRateLimitError as e:

            raise RateLimitError(
                str(e)
            ) from e

        except APIConnectionError as e:

            raise ProviderError(
                str(e)
            ) from e

        except APIError as e:

            raise ProviderError(
                str(e)
            ) from e

        except InferenceError:

            raise

        except Exception as e:

            raise InferenceError(
                str(e)
            ) from e