from abc import ABC, abstractmethod

class Memory(ABC):

    @abstractmethod
    def get(self, key: str):
        ...

    @abstractmethod
    def set(self, key: str, value):
        ...

