from mcptool.tool_manager import ToolManager


class ExpenseLoggerAgent:
    """Calls the log_expense tool and returns the result as context for the orchestrator."""

    TOOL_NAME = "log_expense"

    def __init__(self, tool_manager: ToolManager):
        self._tool_manager = tool_manager

    def handle(self, arguments: dict) -> dict:
        result = self._tool_manager.execute(self.TOOL_NAME, arguments)
        return {"tool_name": self.TOOL_NAME, "arguments": arguments, "result": result}
