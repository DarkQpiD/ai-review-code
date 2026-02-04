import hmac, hashlib, os

def verify_signature(body, signature):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET").encode()
    mac = hmac.new(secret, body, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise Exception("Invalid signature")
