from typing import Dict, Any


class InMemoryMemory:
    def __init__(self):
        self._state: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        return dict(self._state)

    def save(self, state: Dict[str, Any]):
        self._state = dict(state)

