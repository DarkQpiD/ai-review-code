import requests
import os

GITHUB_APP_TOKEN = os.getenv("GITHUB_APP_TOKEN")

def post_pr_comment(repo: str, pr_number: int, body: str):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_APP_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": body}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
