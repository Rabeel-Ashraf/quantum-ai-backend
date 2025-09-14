import pytest
from fastapi.testclient import TestClient
from main import app
from api.dependencies import create_access_token

client = TestClient(app)

def test_chat_endpoint():
    # Create a test token
    token = create_access_token({"sub": "test_user", "plan": "premium"})
    
    # Test the chat endpoint
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello, how are you?", "session_id": "test_session"},
        headers={"Authorization": f"Bearer {token}", "X-API-Key": "test_api_key"}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "tokens_used" in response.json()

def test_stream_chat_endpoint():
    token = create_access_token({"sub": "test_user", "plan": "premium"})
    
    # Test the streaming chat endpoint
    with client.stream(
        "POST",
        "/api/v1/stream_chat",
        json={"message": "Hello, how are you?", "session_id": "test_session"},
        headers={"Authorization": f"Bearer {token}", "X-API-Key": "test_api_key"}
    ) as response:
        assert response.status_code == 200
        # Should receive streaming response

def test_generate_endpoint():
    token = create_access_token({"sub": "test_user", "plan": "premium"})
    
    response = client.post(
        "/api/v1/generate",
        json={"prompt": "Explain quantum computing", "model": "openai"},
        headers={"Authorization": f"Bearer {token}", "X-API-Key": "test_api_key"}
    )
    
    assert response.status_code == 200
    assert "response" in response.json()
    assert "model" in response.json()

def test_api_key_auth():
    # Test without API key
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello", "session_id": "test_session"},
        headers={"Authorization": "Bearer test_token"}
        # No X-API-Key header
    )
    
    assert response.status_code == 401
    assert "API key is required" in response.json()["detail"]
