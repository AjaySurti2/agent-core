from abc import ABC, abstractmethod
from typing import Dict, Any, List, ClassVar


class BaseTool(ABC):
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[Dict[str, Any]]
    keywords: ClassVar[List[str]] = []

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass

