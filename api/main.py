import os
import hmac
import hashlib
import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

GITHUB_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
WORKER_URL = os.getenv("WORKER_URL")


def verify_signature(payload_body, signature_header):
    if not signature_header:
        return False

    sha_name, signature = signature_header.split('=')
    if sha_name != 'sha256':
        return False

    mac = hmac.new(
        GITHUB_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    )

    return hmac.compare_digest(mac.hexdigest(), signature)


@app.post("/webhook/github")
async def github_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()

    if payload.get("action") == "opened" and "pull_request" in payload:
        print("PR opened → sending to worker")

        requests.post(WORKER_URL, json=payload)

    return {"status": "ok"}