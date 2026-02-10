import pytest

from agent_core.tools.base import BaseTool
from agent_core.tools.registry import ToolRegistry
from agent_core.agent.executor import ToolExecutor, MemoryAwareChainExecutor
from agent_core.agent.memory_manager import MemoryManager
from agent_core.memory.in_memory import InMemoryStore


# -------------------------
# Dummy Tools for Testing
# -------------------------

class SuccessTool(BaseTool):
    name = "success_tool"
    description = "Always succeeds"
    input_schema = {}
    keywords = []

    def run(self, **kwargs):
        return "ok"


class FailingTool(BaseTool):
    name = "failing_tool"
    description = "Always fails"
    input_schema = {}
    keywords = []

    def run(self, **kwargs):
        raise RuntimeError("forced failure")


# -------------------------
# Helper Setup
# -------------------------

def build_executor():
    registry = ToolRegistry()
    registry.register(SuccessTool())
    registry.register(FailingTool())

    tool_executor = ToolExecutor(registry)
    memory = MemoryManager(InMemoryStore())

    return MemoryAwareChainExecutor(tool_executor, memory), memory


# -------------------------
# Tests
# -------------------------

def test_successful_tool_execution():
    executor, memory = build_executor()

    plan = {
        "steps": [
            {"tool": "success_tool", "arguments": {}}
        ]
    }

    results = executor.execute_plan(plan)

    assert len(results) == 1
    assert results[0]["success"] is True
    assert results[0]["output"] == "ok"


def test_failing_tool_execution():
    executor, memory = build_executor()

    plan = {
        "steps": [
            {"tool": "failing_tool", "arguments": {}}
        ]
    }

    results = executor.execute_plan(plan)

    assert len(results) == 1
    assert results[0]["success"] is False
    assert "forced failure" in results[0]["error"]


def test_chain_stops_on_failure():
    executor, memory = build_executor()

    plan = {
        "steps": [
            {"tool": "failing_tool", "arguments": {}},
            {"tool": "success_tool", "arguments": {}},
        ]
    }

    results = executor.execute_plan(plan)

    # Should stop after first failure
    assert len(results) == 1
    assert results[0]["success"] is False


def test_memory_records_execution():
    executor, memory = build_executor()

    plan = {
        "steps": [
            {"tool": "success_tool", "arguments": {}}
        ]
    }

    executor.execute_plan(plan)

    records = memory.get_recent()
    assert len(records) >= 1
    assert records[-1]["tool"] == "success_tool"
