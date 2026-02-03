import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_APP_TOKEN = os.getenv("GITHUB_APP_TOKEN")
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
