# FastAPI LiteLLM Gemma Integration

This project demonstrates how to integrate LiteLLM with a FastAPI application to use the Gemma model from HuggingFace. It provides an API endpoint to send prompts to the model and receive responses.

## Features

- FastAPI for creating the API.
- LiteLLM for interacting with various LLMs.
- Gemma model running via Ollama as the language model. (Previously HuggingFace)
- Unit tests for all functionalities.

**Note on Ollama Setup:** This project now uses Ollama to serve the LLM locally. You need to have Ollama installed and running, and the desired model (e.g., `gemma:latest`) pulled. Visit [https://ollama.com](https://ollama.com) for installation instructions.

## Project Structure

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── tests
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
└── README.md
```

## Setup and Installation

(Instructions to be added once the project is further developed)

## Running the Application

(Instructions to be added once the project is further developed)

##Running Tests

(Instructions to be added once the project is further developed)
```
