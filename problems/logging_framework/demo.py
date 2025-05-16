from log_level import LogLevel
from logger import Logger
from file_appender import FileAppender
from logger_config import LoggerConfig

def func():
    logger = Logger.get_instance()
    logger.log(LogLevel.DEBUG, "This is a debug message.")
    logger.log(LogLevel.INFO, "This is an info message.")
    logger.log(LogLevel.WARNING, "This is a warning message.")

    config = LoggerConfig(LogLevel.DEBUG, FileAppender("app.log"))
    logger.set_config(config)
    logger.log(LogLevel.ERROR, "This is an error message.")


if __name__ == "__main__":
    func()