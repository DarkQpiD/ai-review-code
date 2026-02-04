import os
from fastapi import FastAPI
from google import genai

from github import comment_pr
from prompt import PROMPT

# --- Init Gemini client ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()


@app.post("/review")
async def review(payload: dict):
    diff = "TODO: fetch diff from GitHub API"

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=PROMPT.format(diff=diff),
    )

    review_text = response.text
    comment_pr(payload, review_text)

    return {"reviewed": True}
