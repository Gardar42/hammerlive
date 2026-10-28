"""Сервис Identity ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive Identity", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "identity", "status": "ok"}
