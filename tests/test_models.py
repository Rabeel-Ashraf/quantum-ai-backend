import pytest
from models.schemas import ChatRequest, GenerateRequest

def test_chat_request_schema():
    request = ChatRequest(
        message="Hello, how are you?",
        session_id="test_session_123"
    )
    
    assert request.message == "Hello, how are you?"
    assert request.session_id == "test_session_123"

def test_generate_request_schema():
    request = GenerateRequest(
        prompt="Explain quantum computing",
        model="openai",
        apply_uae_template=True
    )
    
    assert request.prompt == "Explain quantum computing"
    assert request.model == "openai"
    assert request.apply_uae_template == True

def test_generate_request_defaults():
    request = GenerateRequest(
        prompt="Test prompt"
    )
    
    assert request.model is None
    assert request.apply_uae_template == False
