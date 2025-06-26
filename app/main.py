from fastapi import FastAPI
from pydantic import BaseModel
from litellm import acompletion  # Correct async method
import os

app = FastAPI()

# Change this to match the Ollama model you’ve pulled (e.g., gemma:2b, mistral:7b, etc.)
OLLAMA_MODEL_NAME = "ollama/qwen2.5:3b"

@app.get("/")
async def root():
    return {"message": "Welcome to the Local LLM API powered by LiteLLM + Ollama!"}

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

class PromptInput(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_response(request: PromptInput):
    try:
        response = await acompletion(
            model=OLLAMA_MODEL_NAME,
            messages=[{"role": "user", "content": request.prompt}]
        )

        content = (
            response.choices[0].message.content.strip()
            if response.choices and response.choices[0].message and response.choices[0].message.content
            else "Error: Invalid response format from model."
        )
        return {"response": content}

    except Exception as e:
        print(f"LiteLLM/Ollama Error: {e}")
        return {"error": f"Failed to generate response: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)