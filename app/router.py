import time
import os
import re
import httpx
from app.models import ModelResponse
from dotenv import load_dotenv

load_dotenv()

COST_MAP = {
    "llama-3.1-8b-instant": 0.0001,
    "llama-3.3-70b-versatile": 0.0008,
    "groq/compound": 0.0006,
}

async def call_groq_model(prompt: str, max_tokens: int, model: str) -> ModelResponse:
    api_key = os.getenv("GROQ_API_KEY")
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                },
            )
            data = response.json()
            print(f"[{model}] Status: {response.status_code}")

            if response.status_code != 200:
                raise Exception(f"API error {response.status_code}: {data.get('error', {}).get('message', str(data))}")

            text = data["choices"][0]["message"]["content"]
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
            latency = round(time.time() - start, 3)
            tokens = data.get("usage", {}).get("total_tokens", 0)
            cost = round((tokens / 1000) * COST_MAP[model], 6)
            return ModelResponse(
                model=model,
                provider="Groq",
                response=text,
                latency_seconds=latency,
                estimated_cost_usd=cost,
            )
    except Exception as e:
        return ModelResponse(
            model=model,
            provider="Groq",
            response=f"Error: {str(e)}",
            latency_seconds=round(time.time() - start, 3),
            estimated_cost_usd=0.0,
        )

async def call_groq(prompt: str, max_tokens: int) -> ModelResponse:
    return await call_groq_model(prompt, max_tokens, "llama-3.1-8b-instant")

async def call_openai(prompt: str, max_tokens: int) -> ModelResponse:
    return await call_groq_model(prompt, max_tokens, "llama-3.3-70b-versatile")

async def call_anthropic(prompt: str, max_tokens: int) -> ModelResponse:
    return await call_groq_model(prompt, max_tokens, "groq/compound")