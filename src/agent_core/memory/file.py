import json
from pathlib import Path
from agent_core.memory.base import Memory


class FileMemory(Memory):
    def __init__(self, path: str = ".agent_memory.json"):
        self.path = Path(path)
        self._store = {}

        if self.path.exists():
            self._load()

    def _load(self):
        with self.path.open("r", encoding="utf-8") as f:
            self._store = json.load(f)

    def _save(self):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value):
        self._store[key] = value
        self._save()
