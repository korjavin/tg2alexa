from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from shared.config import settings
import redis
from fastapi import APIRouter

# Initialize Redis connection
redis_client = redis.from_url(settings.REDIS_URL)

# Create FastAPI router
telegram_router = APIRouter()

async def start_command(update: Update, context):
    await update.message.reply_text(
        "Hello! I'm your Telegram to Alexa bridge. "
        "Any message you send here will be read by your Alexa devices."
    )

async def handle_message(update: Update, context):
    message = update.message.text
    redis_client.rpush("telegram_messages", message)
    await update.message.reply_text("Message received and queued for Alexa!")

# Webhook endpoint
@telegram_router.post("/")
async def webhook(update: Update):
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    await application.initialize()
    await application.process_update(update)
    return {"status": "ok"}