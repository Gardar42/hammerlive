"""Сервис VideoStreamer ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive VideoStreamer", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "video-streamer", "status": "ok"}
