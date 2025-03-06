import json
import pytest
from unittest.mock import patch, MagicMock
from time import sleep

# Use absolute import from `src`
from src.llm_client import LLMClient

@pytest.fixture
def llm_client():
    """Fixture to create an LLMClient instance for testing."""
    return LLMClient()

@patch("requests.post")
def test_call_deepseek(mock_post, llm_client):
    """Test calling DeepSeek API (mocked)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "DeepSeek Test Response"}}]
    }
    
    mock_post.return_value = mock_response
    
    response = llm_client._call_deepseek("System Message", "User Message")
    response_body = json.loads(response["body"])
    
    assert response["statusCode"] == 200
    assert response_body["response"] == "DeepSeek Test Response"

@patch("requests.post")
def test_call_openai(mock_post, llm_client):
    """Test calling OpenAI API (mocked)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "OpenAI Test Response"}}]
    }
    
    mock_post.return_value = mock_response
    
    response = llm_client._call_openai("System Message", "User Message")
    response_body = json.loads(response["body"])
    
    assert response["statusCode"] == 200
    assert response_body["response"] == "OpenAI Test Response"

@patch("requests.post")
def test_call_claude(mock_post, llm_client):
    """Test calling Claude (Anthropic) API (mocked)."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Claude Test Response"}}]
    }
    
    mock_post.return_value = mock_response
    
    response = llm_client._call_claude("System Message", "User Message")
    response_body = json.loads(response["body"])
    
    assert response["statusCode"] == 200
    assert response_body["response"] == "Claude Test Response"

@patch("requests.post")
def test_llm_api_error_handling(mock_post, llm_client):
    """Test error handling when API call fails."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    
    mock_post.return_value = mock_response
    
    response = llm_client._call_deepseek("System Message", "User Message")
    response_body = json.loads(response["body"])
    
    assert response["statusCode"] == 500
    assert "error" in response_body
    assert response_body["error"] == "Internal Server Error"

@patch("requests.post")
def test_invalid_provider(mock_post, llm_client):
    """Test invalid LLM provider exception handling."""
    llm_client.provider = "invalid-provider"
    
    with pytest.raises(ValueError, match="❌ Unsupported LLM provider: invalid-provider"):
        llm_client.call_llm("System Message", "User Message")

def test_real_llm_response(llm_client):
    """Test real API call to LLM (DeepSeek/OpenAI) and verify response is received."""
    
    # Test only runs if we have a valid API key
    if not llm_client.api_key:
        pytest.skip("Skipping real API call test: API key is missing.")

    system_message = "You are a pharmacist."
    user_message = "Explain amoxicillin."

    response = llm_client.call_llm(system_message, user_message)
    response_body = json.loads(response["body"])

    # Ensure we got a valid response
    assert response["statusCode"] == 200
    assert "response" in response_body
    assert isinstance(response_body["response"], str)
    assert len(response_body["response"]) > 10  # Basic check that it's not empty

    print("\n✅ Real API Response Received:", response_body["response"])

    # Optional: Delay to avoid hitting rate limits (useful for frequent testing)
    sleep(2)
