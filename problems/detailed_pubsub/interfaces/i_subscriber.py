from abc import ABC, abstractmethod
from typing import Callable
from problems.detailed_pubsub.interfaces.i_message_store import Message

class ISubscriber(ABC):
    """Interface for subscriber"""
    @abstractmethod
    def subscribe(self, topic: str, callback: Callable[[Message], None], from_beginning: bool = False) -> None:
        pass
    
    @abstractmethod
    def unsubscribe(self, topic: str) -> None:
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass