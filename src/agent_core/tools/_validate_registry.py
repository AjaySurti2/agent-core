from agent_core.tools.base import BaseTool


class ToolA(BaseTool):
    name = "tool_a"
    description = "Tool A"
    input_schema = {}
    keywords = ["alpha"]

    def run(self):
        return "A"


class ToolB(BaseTool):
    name = "tool_b"
    description = "Tool B"
    input_schema = {}
    keywords = ["beta"]

    def run(self):
        return "B"