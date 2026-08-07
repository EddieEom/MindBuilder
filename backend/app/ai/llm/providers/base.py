from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(

        self,

        *,

        system: str,

        user: str,

        profile: str,

    ) -> str:
        """
        LLM API 호출.

        Returns
        -------
        str
            LLM Raw Text
        """
        raise NotImplementedError