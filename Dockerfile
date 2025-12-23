FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# IMPORTANT:
# Do NOT start uvicorn here
# Fly will start it via fly.toml processes



