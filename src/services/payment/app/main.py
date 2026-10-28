"""Сервис Payment ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive Payment", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "payment", "status": "ok"}
