"""Сервис BidTracker ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive BidTracker", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "bid-tracker", "status": "ok"}
