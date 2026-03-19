from ollama import AsyncClient

async def generate_routed_response(prompt: str, route_name: str) -> dict:
    if route_name == "tier_1_complex":
        target_model = "llama3"
    else:
        target_model = "qwen2.5:0.5b"
    
    print(f"Executing prompt on {target_model}...")
    
    client = AsyncClient()
    
    response = await client.chat(
        model = target_model,
        messages = [
            {"role": "user", "content": prompt}
        ],
        keep_alive = 0
    )
    
    return {
        "content": response['message']['content'],
        "model_used": target_model
    }
    