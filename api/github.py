import hmac
import hashlib
import requests
from settings import WEBHOOK_SECRET, GITHUB_APP_TOKEN

def verify_signature(body: bytes, signature: str) -> bool:
    if not signature or not WEBHOOK_SECRET:
        return False

    mac = hmac.new(
        WEBHOOK_SECRET.encode(),
        msg=body,
        digestmod=hashlib.sha256
    )
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)


def get_pr_diff(repo: str, pr_number: int) -> str:
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {GITHUB_APP_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text
