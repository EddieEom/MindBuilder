import json
import re
from typing import Any

from app.ai.llm.exceptions import InvalidJSONError


class LLMParser:
    """
    OpenRouter / LLM 응답을 JSON으로 변환한다.
    """

    @staticmethod
    def parse(text: str) -> dict[str, Any]:

        if not text:

            raise InvalidJSONError("LLM returned empty response.")

        text = text.strip()

        # markdown 제거
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.MULTILINE,
        )

        text = re.sub(
            r"```$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # JSON 영역 추출
        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:

            raise InvalidJSONError(
                "JSON object not found."
            )

        text = text[start:end + 1]

        try:

            return json.loads(text)

        except json.JSONDecodeError as e:

            raise InvalidJSONError(
                str(e)
            ) from e