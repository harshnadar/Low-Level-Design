from abc import ABC, abstractmethod

class LogAppender(ABC):
    @abstractmethod
    def append(self, message: str) -> None:
        """Append a log message to the appender."""
        pass