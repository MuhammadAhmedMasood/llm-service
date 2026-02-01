from pathlib import Path


class PromptNotFoundError(Exception):
    pass


class PromptLoader:
    def __init__(self, base_path: str = "prompts"):
        self.base_path = Path(base_path)

    def load(
        self,
        task: str,
        version: str = "v1"
    ) -> str:
        prompt_path = self.base_path / task / f"{version}.txt"

        if not prompt_path.exists():
            raise PromptNotFoundError(
                f"Prompt not found: {task}/{version}"
            )

        return prompt_path.read_text(encoding="utf-8")
