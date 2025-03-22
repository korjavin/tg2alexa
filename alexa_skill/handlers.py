from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from shared.config import settings
import redis

# Initialize Redis connection
redis_client = redis.from_url(settings.REDIS_URL)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to Telegram to Alexa. You can ask me to read your messages."
        return handler_input.response_builder.speak(speech_text).response

class ReadMessagesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ReadMessagesIntent")(handler_input)

    def handle(self, handler_input):
        messages = redis_client.lrange("telegram_messages", 0, -1)
        if messages:
            speech_text = "Here are your messages: " + ". ".join([msg.decode() for msg in messages])
            redis_client.delete("telegram_messages")
        else:
            speech_text = "You have no new messages."
            
        return handler_input.response_builder.speak(speech_text).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

# Skill Builder
sb = SkillBuilder()

# Register handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReadMessagesIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Create FastAPI router
from fastapi import APIRouter
alexa_router = APIRouter()

@alexa_router.post("/")
async def alexa_endpoint(request: dict):
    return sb.lambda_handler()(request, None)