"""Сервис TelegramAdapter ИС HammerLive (заготовка)."""
from fastapi import FastAPI

app = FastAPI(title="HammerLive TelegramAdapter", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"service": "telegram-adapter", "status": "ok"}
