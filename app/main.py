from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import time

from app.core.router_engine import router
from app.services.llm_services import generate_routed_response
from app.database.connection import init_db, log_request

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up: Initializing Database...")
    init_db()
    yield

app = FastAPI(title="CostLLM API", lifespan=lifespan)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/v1/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.perf_counter()
    
    match = router(request.prompt)
    route_name = match.name if match else "unmatched"
    
    result = await generate_routed_response(request.prompt, route_name)
    
    end_time = time.perf_counter()
    
    log_request(
        prompt=request.prompt,
        routed_tier = route_name,
        model_used = result['model_used']
    )
    
    return {
        "original_prompt": request.prompt,
        "routed_tier": route_name,
        "model_used": result["model_used"],
        "routing_time_seconds": round(end_time - start_time, 4),
        "response": result["content"]
    }
