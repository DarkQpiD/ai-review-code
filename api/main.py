from fastapi import FastAPI, Request, Header
from redis import Redis
import json
from github import verify_signature, get_pr_diff
from settings import REDIS_HOST, REDIS_PORT

app = FastAPI()
redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None)
):
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        return {"error": "invalid signature"}

    payload = await request.json()

    if payload.get("action") not in ["opened", "synchronize"]:
        return {"status": "ignored"}

    repo = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]

    diff = get_pr_diff(repo, pr_number)

    job = {
        "repo": repo,
        "pr_number": pr_number,
        "diff": diff
    }

    redis.rpush("review-queue", json.dumps(job))
    return {"status": "queued"}
