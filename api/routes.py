from fastapi import APIRouter
from api.schemas import (
    GenerateRequest, GenerateResponse,
    SummariseRequest, SummariseResponse,
    ClassifyRequest, ClassifyResponse, LLMRequestLog
)
from core.prompt_loader import PromptLoader
from core.prompt_renderer import PromptRenderer
from core.model_router import ModelRouter
from core.telemetry import log_request, LLM_LOGS
from typing import List
from core.evaluator import SimpleEvaluator
from core.evaluations import store_evaluation
from api.schemas import EvaluationResult
from core.evaluations import EVALUATIONS

prompt_loader = PromptLoader()
prompt_renderer = PromptRenderer()
model_router = ModelRouter()

router = APIRouter()

'''
@router.post("/v1/generate", response_model=GenerateResponse)
def generate_text(request: GenerateRequest):
    return GenerateResponse(
        output="PLACEHOLDER_RESPONSE",
        metadata={
            "model": "not_selected",
            "prompt_version": request.prompt_version,
            "tokens_used": 0,
            "estimated_cost_usd": 0.0,
            "latency_ms": 0
        }
    )
'''
@router.post("/v1/generate", response_model=GenerateResponse)
def generate_text(request: GenerateRequest):
    template = prompt_loader.load(
        task="generate",
        version=request.prompt_version
    )

    prompt = prompt_renderer.render(
        template,
        {
            "task": request.task,
            "input": request.input,
            "constraints": request.constraints or "None"
        }
    )
    
    model = model_router.select_model(request.task, request.mode)
    temperature = 0.0 if request.mode == "deterministic" else 0.7

    result = model_router.call_model(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=request.constraints.get("max_tokens", 300)
        if request.constraints else 300
    )
    
    cost = round(result["tokens_used"] / 1000 * 0.002, 6)
    
    log = log_request(
        task=request.task,
        model=result["model"],
        prompt_version=request.prompt_version,
        mode=request.mode,
        tokens_used=result["tokens_used"],
        cost=cost,
        latency=result["latency_ms"],
        input_text=request.input,
        output_text=result["output"]
    )
    
    evaluator = SimpleEvaluator()
    eval_result = evaluator.evaluate(
        task=request.task,
        input_text=request.input,
        output_text=result["output"]
    )
    
    store_evaluation(
        EvaluationResult(
            request_id=log.request_id if hasattr(log, "request_id") else "latest",
            score=eval_result["score"],
            criteria=eval_result["criteria"],
            evaluator=eval_result["evaluator"]
        )
    )

    return GenerateResponse(
        output=result["output"],
        metadata={
            "model": result["model"],
            "prompt_version": request.prompt_version,
            "tokens_used": result["tokens_used"],
            "estimated_cost_usd": cost,
            "latency_ms": result["latency_ms"],
            "mode": request.mode
        }
    )


@router.post("/v1/summarise", response_model=SummariseResponse)
def summarise_text(request: SummariseRequest):
    template = prompt_loader.load(
        task="summarise",
        version="v1"
    )
    
    prompt = prompt_renderer.render(
        template,
        {
            "input": request.input
        }
    )
    
    model = model_router.select_model("summarise", request.mode)
    temperature = 0.0

    result = model_router.call_model(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=200
    )
    
    cost = round(result["tokens_used"] / 1000 * 0.002, 6)

    log_request(
        task="summarise",
        model=result["model"],
        prompt_version="v1",
        mode=request.mode,
        tokens_used=result["tokens_used"],
        cost=cost,
        latency=result["latency_ms"],
        input_text=request.input,
        output_text=result["output"]
    )
    
    return SummariseResponse(
        summary=result["output"],
        metadata={
            "model": result["model"],
            "tokens_used": result["tokens_used"],
            "estimated_cost_usd": cost,
            "latency_ms": result["latency_ms"]
        }
    )


@router.post("/v1/classify", response_model=ClassifyResponse)
def classify_text(request: ClassifyRequest):
    
    template = prompt_loader.load(
        task="classify",
        version="v1"
    )
    
    prompt = prompt_renderer.render(
        template,
        {
            "input": request.input,
            "labels": ", ".join(request.labels)
        }
    )

    model = model_router.select_model("classify", "deterministic")

    result = model_router.call_model(
        model=model,
        prompt=prompt,
        temperature=0.0,
        max_tokens=50
    )
    
    cost = round(result["tokens_used"] / 1000 * 0.002, 6)

    log_request(
        task="classify",
        model=result["model"],
        prompt_version="v1",
        mode="deterministic",
        tokens_used=result["tokens_used"],
        cost=cost,
        latency=result["latency_ms"],
        input_text=request.input,
        output_text=result["output"]
    )
    
    return ClassifyResponse(
        label=result["output"].strip(),
        confidence=0.8,
        metadata={
            "model": result["model"],
            "tokens_used": result["tokens_used"],
            "estimated_cost_usd": cost,
            "latency_ms": result["latency_ms"]
        }
    )
    
@router.get("/v1/telemetry", response_model=List[LLMRequestLog])
def get_telemetry():
    return LLM_LOGS

@router.get("/v1/evaluations", response_model=list[EvaluationResult])
def get_evaluations():
    return EVALUATIONS
