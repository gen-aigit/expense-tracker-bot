from openai import OpenAI

from prompt.direct_response_prompt import DIRECT_RESPONSE_SYSTEM_PROMPT

MODEL = "gpt-4o-mini"


class DirectResponseGenAgent:
    """Generates a response directly from the OpenAI LLM for queries that
    did not require any tool call."""

    def __init__(self, client: OpenAI):
        self._client = client

    def generate(self, query: str) -> str:
        response = self._client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": DIRECT_RESPONSE_SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content
