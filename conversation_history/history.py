from typing import List

from db_utils.mongodb_client import get_client

DATABASE_NAME = "ai_database"
COLLECTION_NAME = "chat_history"

# Only the most recent N exchanges are replayed into an agent's message history.
# Keeping this bounded avoids diluting/contradicting the system prompt as a
# conversation grows, and stops every request from resending the entire
# lifetime chat log.
MAX_TURN_HISTORY_SIZE = 6


def add_history(payload: dict) -> None:
    """Insert a user/assistant exchange into the chat_history collection."""
    client = get_client()
    collection = client[DATABASE_NAME][COLLECTION_NAME]
    collection.insert_one(payload)


def get_history(limit: int = MAX_TURN_HISTORY_SIZE) -> List[dict]:
    """Fetch the most recent `limit` conversation exchanges, oldest first."""
    client = get_client()
    collection = client[DATABASE_NAME][COLLECTION_NAME]
    recent = list(collection.find().sort("_id", -1).limit(limit))
    recent.reverse()
    return recent
