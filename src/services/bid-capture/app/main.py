"""Сервис BidCapture ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive BidCapture", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "bid-capture", "status": "ok"}
