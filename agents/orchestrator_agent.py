from typing import List

from agents.budget_info_agent import BudgetInfoAgent
from agents.expense_logger_agent import ExpenseLoggerAgent
from agents.expense_summary_agent import ExpenseSummaryAgent
from agents.update_budget_agent import UpdateBudgetAgent
from agents.set_budget_agent import SetBudgetAgent


class OrchestratorAgent:
    """Routes each planned tool call to the matching downstream agent
    (expense_logger_agent, expense_summary_agent, budget_info_agent,
    update_budget_agent) and collects their results into a single context list."""

    def __init__(
        self,
        expense_logger_agent: ExpenseLoggerAgent,
        expense_summary_agent: ExpenseSummaryAgent,
        budget_info_agent: BudgetInfoAgent,
        update_budget_agent: UpdateBudgetAgent,
        set_budget_agent: SetBudgetAgent,
    ):
        self._routes = {
            ExpenseLoggerAgent.TOOL_NAME: expense_logger_agent,
            ExpenseSummaryAgent.TOOL_NAME: expense_summary_agent,
            BudgetInfoAgent.TOOL_NAME: budget_info_agent,
            UpdateBudgetAgent.TOOL_NAME: update_budget_agent,
            SetBudgetAgent.TOOL_NAME: set_budget_agent,
        }

    def handle(self, tool_calls: List[dict]) -> List[dict]:
        context = []
        for call in tool_calls:
            tool_name = call.get("tool_name")
            arguments = call.get("arguments", {})
            print("orchestrator toolname:",tool_name)
            print("orchestrator args:",arguments)
            agent = self._routes.get(tool_name)
            if agent is None:
                context.append({
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": f"error: no agent registered for tool '{tool_name}'",
                })
                continue
            context.append(agent.handle(arguments))
        return context
