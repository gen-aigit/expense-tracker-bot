import json
import os

import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

EXPENSE_API_BASE_URL = os.getenv("EXPENSE_API_BASE_URL", "http://localhost:8080")


def log_expense(amount: float, category: str, description: str = "", date: str = "") -> str:
    """Log a new expense via POST /api/expense."""
    url = f"{EXPENSE_API_BASE_URL}/api/expense"
    payload = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        return json.dumps({"error": str(exc)})


def get_spending_summary(category: str = "", start_date: str = "", end_date: str = "") -> str:
    """Fetch a spending summary via GET /api/expense/summary."""
    url = f"{EXPENSE_API_BASE_URL}/api/expense/summary"
    params = {
        "category": category,
        "start_date": start_date,
        "end_date": end_date,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        return json.dumps({"error": str(exc)})


def check_budget_status(category: str) -> str:
    """Fetch budget status for a category via GET /api/budget/info."""
    url = f"{EXPENSE_API_BASE_URL}/api/budget/info"
    params = {"category": category}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        return json.dumps({"error": str(exc)})


def update_budget(category: str, monthly_limit: float) -> str:
    """Create/update a monthly budget limit via PUT /api/budget/update."""
    

    url = f"{EXPENSE_API_BASE_URL}/api/budget/update"
    payload = {
        "category": category,
        "monthly_limit": monthly_limit,
        "updated_date": datetime.now().strftime("%d/%m/%Y"),
    }
    try:
        response = requests.put(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        return json.dumps({"error": str(exc)})
    

def set_budget(category: str, monthly_limit: float) -> str:
    """Create a monthly budget limit via PPOST /api/budget"""
    

    url = f"{EXPENSE_API_BASE_URL}/api/budget"
    payload = {
        "category": category,
        "monthly_limit": monthly_limit,
        "updated_date": datetime.now().strftime("%d/%m/%Y"),
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        return json.dumps({"error": str(exc)})



class ToolManager:
    """Owns the tool implementations, their OpenAI function-calling schemas,
    and dispatches execution by tool name (t1..t4)."""

    _TOOLS = {
        "log_expense": log_expense,
        "get_spending_summary": get_spending_summary,
        "check_budget_status": check_budget_status,
        "update_budget": update_budget,
        "set_budget":set_budget
    }

    _SCHEMAS = [
        {
            "type": "function",
            "function": {
                "name": "log_expense",
                "description": "Record a new expense the user made.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "The expense amount."},
                        "category": {"type": "string", "description": "Expense category, e.g. grocery, movie, rent,vehicle,transportation,food."},
                        "description": {"type": "string", "description": "Short free-text description of what the expense was for (item, merchant, or occasion), e.g. 'lunch with coworkers' or 'Uber ride'. Derive this from the user's message whenever possible instead of leaving it empty."},
                        "date": {"type": "string", "description": "Date of the expense in YYYY-MM-DD format. Omit if not provided."},
                    },
                    "required": ["amount", "category"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_spending_summary",
                "description": "Get a summary/breakdown of the user's spending, optionally filtered by category and/or date range.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category to filter by. Omit for all categories."},
                        "start_date": {"type": "string", "description": "optional,Start date in YYYY-MM-DD format."},
                        "end_date": {"type": "string", "description": "optional,End date in YYYY-MM-DD format."},
                    },
                    "required": ["category"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "check_budget_status",
                "description": "Check the current budget status (limit, spent, remaining) for a category.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category to check the budget for,like  e.g. grocery, movie, rent,vehicle,transportation,food."},
                    },
                    "required": ["category"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_budget",
                "description": "Set or update the monthly budget limit for a category.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category to update the budget for."},
                        "monthly_limit": {"type": "number", "description": "The new monthly budget limit."},
                    },
                    "required": ["category", "monthly_limit"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "set_budget",
                "description": "Set/add  the new monthly budget limit for a category.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Category to set the budget for."},
                        "monthly_limit": {"type": "number", "description": "The  monthly budget limit."},
                    },
                    "required": ["category", "monthly_limit"],
                },
            },
        },
    ]

    def get_tool_schemas(self) -> list:
        return self._SCHEMAS

    def execute(self, tool_name: str, arguments: dict) -> str:
        tool_fn = self._TOOLS.get(tool_name)
        if tool_fn is None:
            return json.dumps({"error": f"Unknown tool '{tool_name}'"})
        return tool_fn(**arguments)
