# Main FastAPI application file
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LiteLLM Gemma API!"}

from pydantic import BaseModel
from litellm import completion
import os

# Configure LiteLLM to use Gemma.
# For HuggingFace models, LiteLLM typically expects the model name to be prefixed with "huggingface/"
# However, for Gemma, it might be directly supported or need a specific provider syntax if not automatically detected.
# LiteLLM documentation should be consulted for the most up-to-date way to specify HuggingFace models.
# Assuming "huggingface/google/gemma-7b" or similar is the identifier.
# Users might need to set HUGGINGFACE_API_KEY environment variable if the model is not public or requires auth.

# It's good practice to load sensitive keys or model names from environment variables.
# For this example, we'll hardcode it for simplicity, but in a real app, use os.getenv.
# GEMMA_MODEL_NAME = "huggingface/google/gemma-2b" # Using a smaller version for easier testing; adjust as needed.
# Switched to Ollama. Ensure Ollama is running and the model is pulled (e.g., `ollama pull gemma:latest`)
GEMMA_MODEL_NAME = "ollama/gemma:latest" # Or your specific Ollama model name

async def get_llm_response(prompt_text: str) -> str:
    """
    Sends a prompt to the configured Gemma model via LiteLLM and returns the response.
    """
    try:
        messages = [{"role": "user", "content": prompt_text}]
        response = await completion( # Use acompletion for async FastAPI
            model=GEMMA_MODEL_NAME,
            messages=messages
        )
        # The response object structure depends on LiteLLM's version and the model.
        # Typically, the content is in response.choices[0].message.content
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            # Log the full response for debugging if the expected structure is not found
            print(f"Unexpected LiteLLM response structure: {response}")
            return "Error: Could not parse response from LLM."
    except Exception as e:
        print(f"Error interacting with LiteLLM: {e}")
        # In a real app, you'd have more robust error handling and logging.
        return f"Error: An exception occurred while processing your request: {str(e)}"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/prompt")
async def generate_response_endpoint(request: PromptRequest):
    """
    FastAPI endpoint to get a response from the Gemma model.
    """
    model_response = await get_llm_response(request.prompt)
    return {"response": model_response}
