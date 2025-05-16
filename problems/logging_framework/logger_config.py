from log_appender import LogAppender
from log_level import LogLevel
from typing import List

class LoggerConfig:
    def __init__(self, log_level: LogLevel, log_appender: LogAppender):
        self.log_appender: LogAppender = log_appender
        self.log_level = log_level  
    
    def set_log_level(self, log_level: LogLevel) -> None:
        """Set the log level."""
        self.log_level = log_level

    def set_log_appender(self, appender: LogAppender) -> None:
        """Add a log appender."""
        self.log_appender.append(appender)

    def get_log_level(self) -> LogLevel:
        """Get the current log level."""
        return self.log_level
    
    def get_log_appender(self) -> LogAppender:
        """Get the list of log appenders."""
        return self.log_appender
    
    
