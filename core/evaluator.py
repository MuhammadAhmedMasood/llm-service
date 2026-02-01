from typing import Dict


class SimpleEvaluator:
    def evaluate(
        self,
        task: str,
        input_text: str,
        output_text: str
    ) -> Dict[str, float]:

        score = 0.0
        reasons = []

        if len(output_text) > 20:
            score += 0.4
            reasons.append("Sufficient length")

        if task == "rewrite" and "Dear" in output_text:
            score += 0.3
            reasons.append("Professional tone detected")

        if output_text.endswith("."):
            score += 0.3
            reasons.append("Well-formed sentence")

        return {
            "score": round(score, 2),
            "criteria": ", ".join(reasons),
            "evaluator": "rule_based_v1"
        }
