from typing import Dict, Any


class PromptRenderer:
    @staticmethod
    def render(
        template: str,
        variables: Dict[str, Any]
    ) -> str:
        rendered = template

        for key, value in variables.items():
            rendered = rendered.replace(
                f"{{{{{key}}}}}",
                str(value)
            )

        return rendered
