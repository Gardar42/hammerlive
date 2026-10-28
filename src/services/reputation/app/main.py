"""Сервис Reputation ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive Reputation", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "reputation", "status": "ok"}
