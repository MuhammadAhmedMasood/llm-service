from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class LLMRequestLog(BaseModel):
    request_id: str
    task: str
    model: str
    prompt_version: str
    mode: str
    tokens_used: int
    estimated_cost_usd: float
    latency_ms: float
    timestamp: datetime
    input_preview: str
    output_preview: str

class GenerateRequest(BaseModel):
    task: str = Field(..., description="Type of generation task")
    input: str = Field(..., description="Input text")
    mode: str = Field("deterministic", description="deterministic | probabilistic")
    prompt_version: Optional[str] = Field("v1")
    constraints: Optional[Dict[str, Any]] = None


class GenerateResponse(BaseModel):
    output: str
    metadata: Dict[str, Any]


class SummariseRequest(BaseModel):
    input: str
    mode: str = "deterministic"


class SummariseResponse(BaseModel):
    summary: str
    metadata: Dict[str, Any]


class ClassifyRequest(BaseModel):
    input: str
    labels: List[str]


class ClassifyResponse(BaseModel):
    label: str
    confidence: float
    metadata: Dict[str, Any]
    
class EvaluationResult(BaseModel):
    request_id: str
    score: float
    criteria: str
    evaluator: str

