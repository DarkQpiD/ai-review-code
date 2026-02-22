FROM python:3.11-slim

WORKDIR /app

COPY worker.py .

RUN pip install fastapi uvicorn requests

CMD ["uvicorn", "worker:app", "--host", "0.0.0.0", "--port", "9000"]