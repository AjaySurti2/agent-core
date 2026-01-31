from abc import ABC, abstractmethod
import logging

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.log = logging.getLogger(f"agent-core.{name}")

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...
