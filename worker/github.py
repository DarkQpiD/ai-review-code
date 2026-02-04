import requests, os

def comment_pr(payload, text):
    pr = payload["pull_request"]
    url = pr["comments_url"]
    token = os.getenv("GITHUB_TOKEN")

    requests.post(
        url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        },
        json={"body": text}
    )
