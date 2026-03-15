from fastapi import FastAPI
from app.models import PromptRequest, RouterResponse
from app.router import call_groq, call_openai, call_anthropic
import asyncio

app = FastAPI(
    title="Multi-LLM Router",
    description="Routes prompts to Claude, OpenAI, and Groq — compares cost and latency",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "running", "project": "Multi-LLM Router by Harwinder Singh"}

@app.post("/route", response_model=RouterResponse)
async def route_prompt(request: PromptRequest):
    results = await asyncio.gather(
        call_groq(request.prompt, request.max_tokens),
        call_openai(request.prompt, request.max_tokens),
        call_anthropic(request.prompt, request.max_tokens),
    )

    results = list(results)
    successful = [r for r in results if not r.response.startswith("Error")]

    fastest = min(successful, key=lambda x: x.latency_seconds).model if successful else results[0].model
    cheapest = min(successful, key=lambda x: x.estimated_cost_usd).model if successful else results[0].model
    recommended = min(successful, key=lambda x: x.latency_seconds + x.estimated_cost_usd * 1000).model if successful else results[0].model

    return RouterResponse(
        prompt=request.prompt,
        results=results,
        fastest_model=fastest,
        cheapest_model=cheapest,
        recommended_model=recommended,
    )

@app.get("/health")
def health():
    return {"status": "healthy"}