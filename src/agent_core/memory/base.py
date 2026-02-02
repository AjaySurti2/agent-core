from abc import ABC, abstractmethod
from typing import Any


class BaseMemory(ABC):
    """
    Abstract base class for agent memory stores.
    """

    @abstractmethod
    def load(self) -> Any:
        pass

    @abstractmethod
    def save(self, data: Any) -> None:
        pass
