import pytest
from fastapi.testclient import TestClient
from main import app
from shared.config import settings
import redis

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def redis_client():
    return redis.from_url(settings.REDIS_URL)

def test_alexa_endpoint(client, redis_client):
    # Setup test data
    redis_client.rpush("telegram_messages", "Test message")
    
    # Test Alexa endpoint
    response = client.post("/alexa", json={
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "test_session",
            "application": {
                "applicationId": settings.ALEXA_APP_ID
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "test_request",
            "intent": {
                "name": "ReadMessagesIntent"
            }
        }
    })
    
    assert response.status_code == 200
    assert "Test message" in response.json()["response"]["outputSpeech"]["text"]
    assert redis_client.llen("telegram_messages") == 0

def test_telegram_webhook(client):
    response = client.post("/telegram", json={
        "update_id": 1,
        "message": {
            "message_id": 1,
            "from": {"id": 1, "first_name": "Test"},
            "chat": {"id": 1},
            "text": "Test message"
        }
    })
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}