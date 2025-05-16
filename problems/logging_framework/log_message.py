from log_level import LogLevel
import time

class LogMessage:
    def __init__(self, log_level: LogLevel, message: str):
        self.log_level = log_level
        self.message = message
        self.timestamp = int(time.time()*1000)

    def get_level(self) -> LogLevel:
        """Get the log level."""
        return self.log_level
    
    def get_message(self) -> str:
        return self.message
    
    def get_timestamp(self) -> int:
        return self.timestamp
    
    def __str__(self) -> str:
        return f"[{self.log_level.name_str}] {self.timestamp}: {self.message}"