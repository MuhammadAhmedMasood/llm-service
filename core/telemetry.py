import uuid
from datetime import datetime
from typing import List
from api.schemas import LLMRequestLog

# Later this can be Postgres / ClickHouse / BigQuery
LLM_LOGS: List[LLMRequestLog] = []


def log_request(
    task: str,
    model: str,
    prompt_version: str,
    mode: str,
    tokens_used: int,
    cost: float,
    latency: float,
    input_text: str,
    output_text: str
):
    log = LLMRequestLog(
        request_id=str(uuid.uuid4()),
        task=task,
        model=model,
        prompt_version=prompt_version,
        mode=mode,
        tokens_used=tokens_used,
        estimated_cost_usd=cost,
        latency_ms=latency,
        timestamp=datetime.utcnow(),
        input_preview=input_text[:120],
        output_preview=output_text[:120]
    )
    LLM_LOGS.append(log)
    return log
