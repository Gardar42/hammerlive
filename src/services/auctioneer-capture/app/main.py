"""Сервис AuctioneerCapture ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive AuctioneerCapture", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "auctioneer-capture", "status": "ok"}
