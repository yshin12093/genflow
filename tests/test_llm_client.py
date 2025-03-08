import json
import pytest
from unittest.mock import patch, MagicMock
from time import sleep

# Use absolute import from `src`
from src.llm_client import LLMClient
from config import LLM_PROVIDER

@pytest.fixture
def llm_client():
    """Fixture to create an LLMClient instance for testing."""
    return LLMClient()

@pytest.fixture
def mock_llm_client():
    """Fixture to create an LLMClient instance with mocked provider."""
    with patch('src.llm_client.LLM_PROVIDER', 'openai'):
        client = LLMClient()
        yield client

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
def test_call_llm_routing(mock_post, llm_client):
    """Test that call_llm correctly routes to the appropriate provider method."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Test Response"}}]
    }
    mock_post.return_value = mock_response
    
    # Test with different providers
    providers = ['deepseek', 'openai', 'anthropic']
    for provider in providers:
        with patch.object(llm_client, 'provider', provider):
            # Mock the specific provider method
            method_name = f'_call_{provider if provider != "anthropic" else "claude"}'
            with patch.object(llm_client, method_name, return_value={"statusCode": 200, "body": json.dumps({"response": f"{provider} response"})}) as mock_method:
                response = llm_client.call_llm("System Message", "User Message")
                
                # Verify the correct method was called
                mock_method.assert_called_once_with("System Message", "User Message")
                response_body = json.loads(response["body"])
                assert response_body["response"] == f"{provider} response"

@patch("requests.post")
def test_invalid_provider(mock_post, llm_client):
    """Test invalid LLM provider exception handling."""
    llm_client.provider = "invalid-provider"
    
    with pytest.raises(ValueError, match="❌ Unsupported LLM provider: invalid-provider"):
        llm_client.call_llm("System Message", "User Message")

@patch('src.llm_client.LLM_PROVIDER', 'invalid-provider')
def test_invalid_provider_initialization():
    """Test invalid LLM provider during initialization."""
    with pytest.raises(ValueError, match="❌ Unsupported LLM provider: invalid-provider"):
        LLMClient()

def test_get_api_key():
    """Test the _get_api_key method for different providers."""
    # Test OpenAI provider
    with patch('src.llm_client.LLM_PROVIDER', 'openai'):
        with patch('src.llm_client.OPENAI_API_KEY', 'test-openai-key'):
            client = LLMClient()
            assert client.api_key == 'test-openai-key'
    
    # Test DeepSeek provider
    with patch('src.llm_client.LLM_PROVIDER', 'deepseek'):
        with patch('src.llm_client.DEEPSEEK_API_KEY', 'test-deepseek-key'):
            client = LLMClient()
            assert client.api_key == 'test-deepseek-key'
    
    # Test Anthropic provider
    with patch('src.llm_client.LLM_PROVIDER', 'anthropic'):
        with patch('src.llm_client.CLAUDE_API_KEY', 'test-claude-key'):
            client = LLMClient()
            assert client.api_key == 'test-claude-key'



    # Optional: Delay to avoid hitting rate limits (useful for frequent testing)
    sleep(2)

@patch("requests.post")
def test_format_response(mock_post):
    """Test the _format_response method with different response types."""
    client = LLMClient()
    
    # Test successful response
    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.json.return_value = {"choices": [{"message": {"content": "Success response"}}]}
    
    success_response = client._format_response(mock_success)
    success_body = json.loads(success_response["body"])
    
    assert success_response["statusCode"] == 200
    assert success_body["response"] == "Success response"
    
    # Test error response
    mock_error = MagicMock()
    mock_error.status_code = 400
    mock_error.text = "Bad Request"
    
    error_response = client._format_response(mock_error)
    error_body = json.loads(error_response["body"])
    
    assert error_response["statusCode"] == 400
    assert error_body["error"] == "Bad Request"
    
    # Test malformed response
    mock_malformed = MagicMock()
    mock_malformed.status_code = 200
    mock_malformed.json.side_effect = ValueError("Invalid JSON")
    
    with patch.object(client, '_format_response', wraps=client._format_response):
        try:
            malformed_response = client._format_response(mock_malformed)
            malformed_body = json.loads(malformed_response["body"])
            assert "error" in malformed_body
        except Exception as e:
            # If an exception is raised, that's also acceptable error handling
            assert "Invalid JSON" in str(e)
