import asyncio

from pydantic import BaseModel

from app.ai.llm.client import LLMClient


class TestSchema(BaseModel):

    message: str

    confidence: float


async def main():

    client = LLMClient()

    response = await client.generate(

        system="""
You are an API server.

You MUST return ONLY valid JSON.

Never use markdown.

Never explain.

Never write text outside JSON.

The response MUST start with {

The response MUST end with }

Output schema

{
    "message": "string",
    "confidence": number
}
""",

        user="Hello",

        schema=TestSchema,

        profile="default",

    )

    print("=" * 60)
    print("RAW")
    print("=" * 60)
    print(response.raw_text)

    print("=" * 60)
    print("PARSED")
    print("=" * 60)
    print(response.parsed)

    print("=" * 60)
    print("VALIDATED")
    print("=" * 60)
    print(response.validated)

    print("=" * 60)
    print("METADATA")
    print("=" * 60)
    print(response.metadata)


if __name__ == "__main__":

    asyncio.run(main())