from logger_config import LoggerConfig
from log_level import LogLevel
from console_log_appender import ConsoleLogAppender
from log_message import LogMessage

class Logger:
    __instance = None

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self
            self.config = LoggerConfig(LogLevel.INFO, ConsoleLogAppender())

    @staticmethod
    def get_instance():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance
    
    def set_config(self, config: LoggerConfig) -> None:
        self.config = config

    def log(self, log_level: LogLevel, message: str) -> None:
        """Log a message with the given log level."""
        if log_level.value >= self.config.get_log_level().value:
            log_message = LogMessage(log_level, message)
            self.config.get_log_appender().append(log_message)  