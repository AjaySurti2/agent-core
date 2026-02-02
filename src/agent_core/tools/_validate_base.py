from agent_core.memory.base import BaseTool


class DummyTool(BaseTool):
    name = "dummy"
    description = "Test tool"
    input_schema = {"x": "int"}

    def run(self, x: int):
        return x * 2
