from agent_core.memory.base import Memory

class InMemoryMemory(Memory):
    def __init__(self):
        self._items = []

    def add(self, item: str):
        self._items.append(item)

    def get_all(self) -> list[str]:
        return self._items.copy()
