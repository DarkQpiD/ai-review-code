# ai-review-code
This repository is for learning how to build an AI-powered code review system using pull request webhooks.

----------------------------------------------------------------
OVERVIEW
----------------------------------------------------------------

AI-powered GitHub Pull Request reviewer using:

-FastAPI (Webhook Server)

-Cloudflare Tunnel (Public URL for local dev)

-OpenRouter API (DeepSeek R1 free model)

-GitHub Webhooks

This system automatically listens to Pull Request events and sends the PR content to an AI model for code review, then posts the result back as a GitHub comment.

----------------------------------------------------------------

ARCHITECTURE FLOW

GitHub Pull Request Event
↓
GitHub Webhook
↓
Cloudflare Tunnel
↓
FastAPI Endpoint (/webhook/github)
↓
OpenRouter API (DeepSeek R1)
↓
Post Comment to GitHub PR

----------------------------------------------------------------

TECH STACK

Python 3.10+
FastAPI
Uvicorn
Requests
Cloudflared
OpenRouter API

----------------------------------------------------------------

INSTALLATION

1.Clone the repository

git clone https://github.com/your-repo/ai-review-bot.git

cd ai-review-bot

2.Create virtual environment

python -m venv venv
source venv/bin/activate

3.Install dependencies

pip install -r requirements.txt

Example requirements.txt:

fastapi
uvicorn
requests
python-dotenv

----------------------------------------------------------------

ENVIRONMENT VARIABLES

Create a .env file in project root:

GITHUB_SECRET=your_webhook_secret
GITHUB_TOKEN=your_github_personal_access_token
OPENROUTER_API_KEY=your_openrouter_api_key

IMPORTANT:
Do NOT commit .env to GitHub.

Add this to .gitignore:

.env

RUN THE SERVER

uvicorn main:app --host 0.0.0.0 --port 8001

If port 8000 is used by Docker, use 8001 or another free port.

START CLOUDFLARE TUNNEL

cloudflared tunnel --url http://localhost:8001

You will receive a public URL like:

https://xxxx.trycloudflare.com

----------------------------------------------------------------

SETUP GITHUB WEBHOOK

Go to:
Repository → Settings → Webhooks → Add webhook

Payload URL:
https://xxxx.trycloudflare.com/webhook/github

Content type:
application/json

Secret:
Use the same value as GITHUB_SECRET

Events:
Select “Pull requests”

----------------------------------------------------------------

OPENROUTER CONFIGURATION

Model used:
deepseek/deepseek-r1-0528:free

API endpoint:
https://openrouter.ai/api/v1/chat/completions

Authorization header:
Bearer OPENROUTER_API_KEY

TESTING WEBHOOK LOCALLY

curl -X POST http://localhost:8001/webhook/github

-H "Content-Type: application/json"
-d '{"test":"hello"}'

If the server responds correctly, your endpoint is working.