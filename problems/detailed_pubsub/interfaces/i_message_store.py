from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import uuid
import time
from typing import Any

@dataclass
class Message:
    """Value object representing a message"""
    topic: str
    data: Any
    message_id: str = None
    timestamp: float = None
    
    def __post_init__(self):
        self.message_id = self.message_id or str(uuid.uuid4())
        self.timestamp = self.timestamp or time.time()

class IMessageStore(ABC):
    """Interface for message storage"""
    @abstractmethod
    def store_message(self, message: Message) -> int:
        pass
    
    @abstractmethod
    def get_messages(self, topic: str, offset: int) -> List[Message]:
        pass
    
    @abstractmethod
    def get_latest_offset(self, topic: str) -> int:
        pass