Cost-Control Smart Model Router (V1: Local MVP)

An intelligent, zero-cost LLM routing middleware built with FastAPI.

This project solves a massive bottleneck in production AI: the cost-to-intelligence ratio. Instead of sending every user prompt to an expensive, heavy model (like GPT-4o or Llama 3 8B), this API intercepts the request, locally evaluates its complexity in milliseconds, and routes it to the most cost-effective model capable of handling the task.

The Problem & The Solution

The Problem: Companies are burning money by using their most expensive, high-parameter models to answer simple queries like "Translate hello to Spanish" or "What is the capital of France?".

The Solution: A proxy API that acts as a triage nurse.

1.  Intercept: The user sends a prompt to the FastAPI backend.
    
2.  Triage (Zero Cost): A local semantic-router uses CPU-based embeddings (fastembed) to classify the intent and complexity of the prompt instantly.
    
3.  Execute: Complex coding and logic prompts are routed to a heavy model (Tier 1). Simple chat and formatting prompts are routed to a tiny, fast model (Tier 3).
    
4.  Log & Save: The system calculates the simulated money saved and logs the transaction to a local SQLite ledger.
    

Tech Stack (V1)

Backend Framework: FastAPI and Uvicorn (Fully asynchronous) Classifier Brain: semantic-router (v1) and fastembed (Runs locally on CPU, no API keys needed) Local LLM Execution: Ollama Python Async Client Models Used: llama3 (8B) for complex logic, math, and coding; and qwen2.5:0.5b as a lightning-fast, lightweight model for simple chat. Database: Python standard sqlite3

Folder Structure

The smart-model-router project contains an app folder, a data folder, and a requirements.txt file.

Inside the app folder, main.py handles the FastAPI application and route definitions. There are also three subfolders:

-   core: Contains router\_engine.py for the semantic routing logic and intent categories.
    
-   services: Contains llm\_services.py for the async Ollama execution logic.
    
-   database: Contains connection.py for SQLite initialization and the cost-savings ledger.
    

The data folder contains the auto-generated router.sqlite database file.

Getting Started

1.  Prerequisites You will need Python 3.9+ and the Ollama application installed on your machine. Pull the required local models via your terminal using the commands "ollama pull llama3" and "ollama pull qwen2.5:0.5b".
    
2.  Installation Clone the repository and install the dependencies using pip install for fastapi, uvicorn, semantic-router, fastembed, ollama, and pydantic.
    
3.  Run the Server Start the FastAPI server from the root directory of the project using the command "uvicorn app.main:app --reload". Upon startup, the app will automatically initialize the data/router.sqlite database if it does not exist.
    
4.  Test the API Navigate to the interactive Swagger UI in your browser at 127.0.0.1:8000/docs. Send a POST request to /v1/chat with a JSON body containing your prompt, such as "Write a Python script for matrix multiplication."
    

The Ledger & Cost Savings

The true value of this router is proving its ROI. Every request processed by the API is logged into a local SQLite database inside the request\_logs table.

The system calculates a simulated savings metric based on the assumption that without a router, all requests would default to the most expensive tier:

-   Tier 1 (Heavy Model): Assumed cost $0.010 per request.
    
-   Tier 3 (Light Model): Assumed cost $0.001 per request.
    

You can check your terminal output to see the live ledger updates, which will look something like: Ledger Updated | Tier: tier\_3\_basic | Saved: $0.009.

Roadmap (V2)

This repository currently represents the Local MVP. Planned upgrades for V2 include:

-   Cloud Provider Integration: Swap Ollama for litellm to route requests dynamically to real OpenAI (GPT-4o) and Groq (Llama 3) endpoints.
    
-   Accurate Token Math: Implement tiktoken to calculate exact cost savings based on input/output token counts rather than a flat simulated fee.
    
-   Fallback Redundancy: Automatic rerouting to a secondary provider (like Gemini) if the primary cloud API experiences downtime.