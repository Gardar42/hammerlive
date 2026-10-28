"""Сервис API Gateway ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive API Gateway", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "api-gateway", "status": "ok"}
