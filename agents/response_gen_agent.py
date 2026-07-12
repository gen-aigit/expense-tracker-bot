import json
from typing import List

from openai import OpenAI

from conversation_history.history import add_history, get_history
from prompt.response_gen_prompt import RESPONSE_GEN_SYSTEM_PROMPT

MODEL = "gpt-4o-mini"


class ResponseGenAgent:
    """Sends the original query plus the orchestrator's context to the OpenAI
    LLM, using a system prompt that turns raw tool results into a natural
    language reply for the user."""

    def __init__(self, client: OpenAI):
        self._client = client

    def generate(self, query: str, context: List[dict]) -> str:
        history_data = get_history()
        #print("history data in response gen agent",history_data)
        messages = self.build_messages(query, context, history_data)

        response = self._client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        answer = response.choices[0].message.content
        self.add_conversation_history(query, answer)
        return answer

    def build_messages(self, query: str, context: str, history: list) -> list:
        messages = [{"role": "system", "content": RESPONSE_GEN_SYSTEM_PROMPT}]

        for entry in history:
            messages.append({"role": entry["role_user"], "content": entry["user_query"]})
            messages.append({"role": entry["role_ai"], "content": entry["ai_response"]})

        messages.append({
            "role": "user",
            "content": f"User question: {query}\n\nTool context: {json.dumps(context, indent=2)}",
        })

        return messages

    def add_conversation_history(self, user_query: str, ai_response: str) -> None:
        add_history({
            "role_user": "user",
            "user_query": user_query,
            "role_ai": "assistant",
            "ai_response": ai_response,
        })
