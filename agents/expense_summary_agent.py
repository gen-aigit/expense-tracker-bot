from mcptool.tool_manager import ToolManager


class ExpenseSummaryAgent:
    """Calls the get_spending_summary tool and returns the result as context for the orchestrator."""

    TOOL_NAME = "get_spending_summary"

    def __init__(self, tool_manager: ToolManager):
        self._tool_manager = tool_manager

    def handle(self, arguments: dict) -> dict:
        result = self._tool_manager.execute(self.TOOL_NAME, arguments)
        return {"tool_name": self.TOOL_NAME, "arguments": arguments, "result": result}
