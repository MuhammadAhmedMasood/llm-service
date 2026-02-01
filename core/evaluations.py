from typing import List
from api.schemas import EvaluationResult

EVALUATIONS: List[EvaluationResult] = []


def store_evaluation(result: EvaluationResult):
    EVALUATIONS.append(result)
