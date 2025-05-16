from enum import Enum

class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

    @property
    def name_str(self) -> str:
        """Return the name of the log level."""
        return self.name.upper()
   
