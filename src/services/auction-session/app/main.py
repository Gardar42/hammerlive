"""Сервис AuctionSession ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive AuctionSession", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "auction-session", "status": "ok"}
