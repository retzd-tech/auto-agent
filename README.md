# FastAPI LiteLLM Gemma Integration

This project demonstrates how to integrate LiteLLM with a FastAPI application to use the Gemma model from HuggingFace. It provides an API endpoint to send prompts to the model and receive responses.

## Features

- FastAPI for creating the API.
- LiteLLM for interacting with various LLMs.
- Gemma model running via Ollama as the language model. (Previously HuggingFace)
- Unit tests for all functionalities.

**Note on Ollama Setup:** This project now uses Ollama to serve the LLM locally. You need to have Ollama installed and running, and the desired model (e.g., `qwen2.5:3b` as configured in `app/main.py`) pulled. You can change the model in `app/main.py` and ensure you have pulled it via `ollama pull <model_name>`. Visit [https://ollama.com](https://ollama.com) for installation instructions.

## Project Structure

```
.
├── .env.example        # Example environment variables
├── .gitignore
├── app
│   ├── __init__.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
└── README.md
```

## Configuration

This project uses a `.env` file to manage configurations, primarily the Ollama model name.

1.  **Create a `.env` file:** Copy the example file:
    ```bash
    cp .env.example .env
    ```
2.  **Edit `.env`:**
    Open the `.env` file and set your desired `OLLAMA_MODEL_NAME`. Ensure the model you specify is available in your local Ollama instance.
    ```env
    OLLAMA_MODEL_NAME="ollama/your-chosen-model:tag"
    ```
    If `OLLAMA_MODEL_NAME` is not set in the `.env` file or as an environment variable, the application will default to `ollama/qwen2.5:3b`.

## Setup and Installation

(Instructions to be added once the project is further developed)

## Running the Application

(Instructions to be added once the project is further developed)

##Running Tests

(Instructions to be added once the project is further developed)
```
