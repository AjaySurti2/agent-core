from agent_core.tools.base import BaseTool


class ToolA(BaseTool):
    """
    Simple tool with no arguments.
    Used to validate successful execution.
    """
    name = "tool_a"
    description = "Tool A (no-arg tool)"
    input_schema = {}
    keywords = ["alpha"]

    def run(self):
        return "A executed"


class ToolB(BaseTool):
    """
    Tool with arguments and failure paths.
    Used to validate executor safety.
    """
    name = "tool_b"
    description = "Tool B (arg-based tool)"
    input_schema = {"x": "int"}
    keywords = ["beta"]

    def run(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")

        if x < 0:
            raise ValueError("x must be non-negative")

        return x * 2
