from abc import ABC, abstractmethod
from typing import Any

class IPublisher(ABC):
    """Interface for publisher"""
    @abstractmethod
    def publish(self, topic: str, data: Any) -> int:
        pass