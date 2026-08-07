import json


class PromptBuilder:

    SYSTEM_PROMPT = """
당신은 MindBuilder AI이다.

절대로 추측하지 않는다.

입력 데이터만 기반으로 분석한다.

항상 JSON만 출력한다.

설명은 한국어로 작성한다.
"""

    @staticmethod
    def build(
        rule_result: dict,
    ) -> str:

        return f"""
다음은 Rule Engine의 결과이다.

{json.dumps(
    rule_result,
    ensure_ascii=False,
    indent=2,
)}

다음 형식으로만 JSON을 출력하라.

{{
    "identity_summary":"",
    "strengths":[],
    "growth_points":[]
}}
"""