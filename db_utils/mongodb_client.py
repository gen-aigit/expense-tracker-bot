import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    """Build and cache a singleton MongoDB client using the URL from .env."""
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        raise RuntimeError("MONGODB_URL is not set. Add it to your .env file.")
    return MongoClient(mongodb_url)



# if __name__ == "__main__":
#     c=get_client()
#     print(c.admin.command('ping'))
#     print("Database initialized successfully.")
