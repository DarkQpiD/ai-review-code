import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")


def get_pr_diff(repo_full_name, pr_number):
    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    response = requests.get(url, headers=headers)
    return response.text


def call_ai(diff_text):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior software engineer reviewing a pull request. Be concise and helpful."
                },
                {
                    "role": "user",
                    "content": f"Review this diff:\n\n{diff_text[:8000]}"
                }
            ]
        }
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]


def comment_on_pr(repo_full_name, pr_number, comment):
    url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    requests.post(url, headers=headers, json={
        "body": f"🤖 AI Code Review\n\n{comment}"
    })


@app.post("/review")
async def review(request: Request):
    payload = await request.json()

    repo = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]

    print(f"Reviewing PR #{pr_number}")

    diff = get_pr_diff(repo, pr_number)
    ai_review = call_ai(diff)
    comment_on_pr(repo, pr_number, ai_review)

    return {"status": "reviewed"}