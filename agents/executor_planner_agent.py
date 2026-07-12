import json
from datetime import date
from typing import List

from openai import OpenAI

from conversation_history.history import get_history
from mcptool.tool_manager import ToolManager
from prompt.tool_calling_prompt import tools_prompt

MODEL = "gpt-4o-mini"


class ExecutorPlannerAgent:
    """Uses the OpenAI SDK's function-calling to decide which tool(s), if any,
    a user query maps to, and extracts the tool name(s) + arguments from the
    model response."""

    def __init__(self, client: OpenAI, tool_manager: ToolManager):
        self._client = client
        self._tool_manager = tool_manager

    def plan(self, query: str) -> List[dict]:
        history_data = get_history()
        print("history data",history_data)
        messages = self.build_messages(query, history_data)
        print("message:",messages)
        response = self._client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=self._tool_manager.get_tool_schemas(),
            tool_choice="auto",
        )

        message = response.choices[0].message
        tool_calls = message.tool_calls or []

        plan = []
        for call in tool_calls:
            try:
                arguments = json.loads(call.function.arguments)
            except (json.JSONDecodeError, TypeError):
                arguments = {}
            plan.append({"tool_name": call.function.name, "arguments": arguments})

        return plan

    def build_messages(self, query: str, history: list) -> list:
        messages = [
            {"role": "system", "content": tools_prompt},
            {"role": "system", "content": f"Current date: {date.today().isoformat()}"},
        ]

        for entry in history:
            messages.append({"role": entry["role_user"], "content": entry["user_query"]})
            messages.append({"role": entry["role_ai"], "content": entry["ai_response"]})

        if history:
            messages.append({
                "role": "system",
                "content": (
                    "Reminder: the turns above are prior conversation history for context only "
                    "(e.g. resolving references like 'that' or a category/date mentioned earlier). "
                    "Judge the newest user message below strictly on its own content against the "
                    "tool-selection rules — do not skip a tool call just because recent turns above "
                    "didn't have one."
                ),
            })

        messages.append({"role": "user", "content": query})

        return messages
