import json


class ResponseParser:

    @staticmethod
    def parse(
        response: str,
    ) -> dict:

        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "JSON not found."
            )

        return json.loads(
            response[
                start:end+1
            ]
        )