"""Сервис VideoCapture ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive VideoCapture", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "video-capture", "status": "ok"}
