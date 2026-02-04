from fastapi import FastAPI, Request, HTTPException
from github import verify_signature
import requests, os

app = FastAPI()

@app.post("/webhook/github")
async def github_webhook(req: Request):
    body = await req.body()
    signature = req.headers.get("X-Hub-Signature-256")

    verify_signature(body, signature)

    payload = await req.json()
    if payload.get("action") not in ["opened", "synchronize"]:
        return {"ignored": True}

    requests.post("http://worker:9000/review", json=payload)
    return {"ok": True}
