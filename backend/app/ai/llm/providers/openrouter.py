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

            raw_text = response.choices[0].message.content

            if raw_text is None:

                raise InferenceError(
                    "LLM returned empty response."
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

        except Exception as e:

            raise InferenceError(
                str(e)
            ) from e