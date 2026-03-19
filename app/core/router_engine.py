from semantic_router import Route
from semantic_router.encoders import FastEmbedEncoder
from semantic_router.routers import SemanticRouter
import sys
import asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from app.services.llm_services import generate_routed_response
import time

tier_1_complex = Route(
    name="tier_1_complex",
    utterances = [
        "Refactor this 500-line React component to use custom hooks and reduce re-renders.",
        "Explain the mathematical intuition behind backpropagation in a transformer model.",
        "Write a Python microservice using FastAPI that implements a RAG architecture with ChromaDB.",
        "Design a PostgreSQL database schema for a high-traffic e-commerce platform.",
        "Analyze this server log and identify the root cause of the memory leak.",
        "Write a comprehensive unit test suite for a custom React Native navigation component."
    ]
)

tier_3_cheap = Route(
    name="tier_3_cheap",
    utterances = [
        "What is the capital of Australia?",
        "Write a short, polite email to my manager asking for next Friday off.",
        "Translate 'hello, how are you' into Spanish.",
        "Give me a recipe for chocolate chip cookies.",
        "What is the weather usually like in December?",
        "Summarize the plot of the Matrix in two sentences."
    ]
)

routes = [tier_1_complex, tier_3_cheap]

encoder = FastEmbedEncoder()

router = SemanticRouter(encoder = encoder, routes = routes)
router.sync("local")

if __name__ == "__main__":
    async def run_test():
        test_prompt = "How can I find factorial of 10?"
    
        start_time = time.perf_counter()
        match = router(test_prompt)
        route_name = match.name if match else "unmatched"
        end_time = time.perf_counter()
    
        print(f"Prompt:'{test_prompt}'")
    
        print(f"Routed to: '{match.name}'")
        print(f"Time taken: {end_time - start_time:.6f} seconds")
    
        result = await generate_routed_response(test_prompt, route_name)
        
        print("\n--- FINAL RESPONSE ---")
        print(f"Model Used: {result['model_used']}")
        print(f"Output:\n{result['content']}")

    asyncio.run(run_test())