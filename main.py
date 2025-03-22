import uvicorn
from fastapi import FastAPI
from alexa_skill.handlers import alexa_router
from telegram_bot.bot import telegram_router
from shared.config import settings

app = FastAPI(title="Telegram to Alexa Integration")

# Include routers
app.include_router(alexa_router, prefix="/alexa")
app.include_router(telegram_router, prefix="/telegram")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )