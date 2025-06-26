import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock # For mocking async functions

from app.main import app, get_llm_response # Import the function to be mocked

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the LiteLLM Gemma API!"}

@pytest.mark.asyncio
async def test_get_llm_response_success():
    """Test the get_llm_response function successfully returns a mocked response."""
    mock_prompt = "Tell me a joke."
    expected_response = "This is a mocked joke."

    # Mock litellm.completion (or acompletion if get_llm_response uses it directly)
    # Since get_llm_response calls litellm.completion, we mock that.
    # The `completion` function from `litellm` is what `app.main.completion` refers to.
    with patch('app.main.completion', new_callable=AsyncMock) as mock_litellm_completion:
        # Configure the mock response object to match LiteLLM's typical structure
        mock_choice = AsyncMock()
        mock_message = AsyncMock()
        mock_message.content = expected_response
        mock_choice.message = mock_message
        
        mock_response_obj = AsyncMock()
        mock_response_obj.choices = [mock_choice]
        
        mock_litellm_completion.return_value = mock_response_obj
        
        actual_response = await get_llm_response(mock_prompt)
        
        assert actual_response == expected_response
        mock_litellm_completion.assert_called_once_with(
            model="ollama/qwen2.5:3b", # Updated to reflect change to Ollama/qwen2.5:3b
            messages=[{"role": "user", "content": mock_prompt}]
        )

@pytest.mark.asyncio
async def test_get_llm_response_litellm_exception():
    """Test the get_llm_response function handles exceptions from LiteLLM."""
    mock_prompt = "This will fail."
    
    with patch('app.main.completion', new_callable=AsyncMock) as mock_litellm_completion:
        mock_litellm_completion.side_effect = Exception("LiteLLM exploded")
        
        actual_response = await get_llm_response(mock_prompt)
        
        assert "Error: An exception occurred while processing your request: LiteLLM exploded" in actual_response
        mock_litellm_completion.assert_called_once()

def test_generate_response_endpoint_success():
    """Test the /prompt endpoint successfully calls get_llm_response and returns its result."""
    mock_prompt_text = "What is FastAPI?"
    expected_llm_response = "FastAPI is a modern, fast (high-performance), web framework for building APIs."

    # We mock the get_llm_response function directly for this endpoint test
    with patch('app.main.get_llm_response', new_callable=AsyncMock) as mock_get_llm_response_func:
        mock_get_llm_response_func.return_value = expected_llm_response
        
        response = client.post("/prompt", json={"prompt": mock_prompt_text})
        
        assert response.status_code == 200
        assert response.json() == {"response": expected_llm_response}
        mock_get_llm_response_func.assert_called_once_with(mock_prompt_text)

def test_generate_response_endpoint_llm_error():
    """Test the /prompt endpoint handles errors from get_llm_response."""
    mock_prompt_text = "Error prompt"
    error_message_from_llm = "Error: Could not parse response from LLM."

    with patch('app.main.get_llm_response', new_callable=AsyncMock) as mock_get_llm_response_func:
        mock_get_llm_response_func.return_value = error_message_from_llm
        
        response = client.post("/prompt", json={"prompt": mock_prompt_text})
        
        assert response.status_code == 200 # The endpoint itself succeeds
        assert response.json() == {"response": error_message_from_llm}
        mock_get_llm_response_func.assert_called_once_with(mock_prompt_text)

def test_generate_response_endpoint_invalid_request():
    """Test the /prompt endpoint with an invalid request body."""
    response = client.post("/prompt", json={"not_a_prompt": "test"})
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation errors
