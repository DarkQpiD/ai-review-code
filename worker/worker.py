import json
import requests
from redis import Redis
from prompt import build_prompt
from github import post_pr_comment
import os

redis = Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379)

while True:
    _, raw = redis.blpop("review-queue")
    job = json.loads(raw)

    repo = job["repo"]
    pr_number = job["pr_number"]
    diff = job["diff"]

    prompt = build_prompt(diff)

    res = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "deepseek-coder:6.7b",
            "prompt": prompt,
            "stream": False
        }
    )
    review = res.json()["response"]

    comment = f"""## 🤖 AI Code Review (DeepSeek)

{review}
"""
    post_pr_comment(repo, pr_number, comment)
