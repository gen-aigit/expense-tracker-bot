from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from agents.budget_info_agent import BudgetInfoAgent
from agents.direct_response_gen_agent import DirectResponseGenAgent
from agents.executor_planner_agent import ExecutorPlannerAgent
from agents.expense_logger_agent import ExpenseLoggerAgent
from agents.expense_summary_agent import ExpenseSummaryAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.response_gen_agent import ResponseGenAgent
from agents.update_budget_agent import UpdateBudgetAgent
from agents.set_budget_agent import SetBudgetAgent
from mcptool.tool_manager import ToolManager
from openAi_client import get_openAiclient

app = FastAPI(title="Expense Tracker Agent System")

client = get_openAiclient()
tool_manager = ToolManager()

executor_planner_agent = ExecutorPlannerAgent(client, tool_manager)
orchestrator_agent = OrchestratorAgent(
    expense_logger_agent=ExpenseLoggerAgent(tool_manager),
    expense_summary_agent=ExpenseSummaryAgent(tool_manager),
    budget_info_agent=BudgetInfoAgent(tool_manager),
    update_budget_agent=UpdateBudgetAgent(tool_manager),
    set_budget_agent=SetBudgetAgent(tool_manager),
)
response_gen_agent = ResponseGenAgent(client)
direct_response_gen_agent = DirectResponseGenAgent(client)


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    tool_calls = executor_planner_agent.plan(request.query)
    print("main",tool_calls)

    if not tool_calls:
        answer = direct_response_gen_agent.generate(request.query)
        return ChatResponse(response=answer)

    context = orchestrator_agent.handle(tool_calls)
    answer = response_gen_agent.generate(request.query, context)
    return ChatResponse(response=answer)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)