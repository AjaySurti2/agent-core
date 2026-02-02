from typing import Any, List
from agent_core.memory.base import BaseMemory


class InMemoryStore(BaseMemory):
    """
    Simple append-only in-memory execution log.
    Used for Phase 20 memory integration.
    """

    def __init__(self):
        self._data: List[Any] = []

    def load(self) -> List[Any]:
        # Return a copy to prevent external mutation
        return list(self._data)

    def save(self, record: Any) -> None:
        self._data.append(record)
