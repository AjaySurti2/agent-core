from abc import ABC, abstractmethod

class Memory(ABC):
    @abstractmethod
    def add(self, item: str):
        pass

    @abstractmethod
    def get_all(self) -> list[str]:
        pass
