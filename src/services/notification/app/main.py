"""Сервис Notification ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive Notification", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "notification", "status": "ok"}
