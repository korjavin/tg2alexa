from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
import os
import redis

# Initialize FastAPI app
app = FastAPI()

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0))
)

# Telegram bot setup
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Alexa skill setup
skill_builder = SkillBuilder()

class MessageHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MessageIntent")(handler_input)

    def handle(self, handler_input):
        user_id = handler_input.request_envelope.session.user.user_id
        message = redis_client.get(f"message:{user_id}")
        
        if message:
            speech_text = f"Your message is: {message.decode('utf-8')}"
            redis_client.delete(f"message:{user_id}")
        else:
            speech_text = "You have no new messages"
            
        return handler_input.response_builder.speak(speech_text).response

skill_builder.add_request_handler(MessageHandler())
skill = skill_builder.create()

@app.post("/telegram")
async def telegram_webhook(update: Update):
    """Handle incoming Telegram messages"""
    user_id = update.message.from_user.id
    message = update.message.text
    
    # Store message in Redis with user ID
    redis_client.set(f"message:{user_id}", message)
    
    return {"status": "ok"}

@app.post("/alexa")
async def alexa_webhook(request: Request):
    """Handle Alexa skill requests"""
    request_data = await request.json()
    response = skill.invoke(request_data)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)