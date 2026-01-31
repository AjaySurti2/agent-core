import json
import os
from typing import Dict, Any


class FileMemory:
    def __init__(self, path: str = ".agent_memory.json"):
        self.path = path

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {}

        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, state: Dict[str, Any]):
        with open(self.path, "w") as f:
            json.dump(state, f, indent=2)
