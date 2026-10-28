"""Сервис BidStreamer ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive BidStreamer", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "bid-streamer", "status": "ok"}
