from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 500

class ModelResponse(BaseModel):
    model: str
    provider: str
    response: str
    latency_seconds: float
    estimated_cost_usd: float

class RouterResponse(BaseModel):
    prompt: str
    results: list[ModelResponse]
    fastest_model: str
    cheapest_model: str
    recommended_model: str
