from log_message import LogMessage

class ConsoleLogAppender:
    def __init__(self):
        pass

    def append(self, message: LogMessage) -> None:
        print(message)