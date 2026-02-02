from typing import Any, TypedDict, List
from agent_core.memory.base import BaseMemory


class MemoryRecord(TypedDict):
    tool: str
    success: bool
    output: Any
    error: str | None


class MemoryManager:
    """
    Manages persistence and retrieval of execution memory.
    """

    def __init__(self, memory: BaseMemory):
        self.memory = memory

    def record_execution(self, record: MemoryRecord) -> None:
        self.memory.save(record)

    def get_recent(self, limit: int = 5) -> List[MemoryRecord]:
        data = self.memory.load()
        return data[-limit:]

