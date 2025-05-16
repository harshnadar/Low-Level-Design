from log_message import LogMessage

class FileAppender:
    def __init__(self, filename):
        self.filename = filename

    def append(self, log_message: LogMessage) -> None:
        with open(self.filename, 'a') as file:
            file.write(str(log_message) + '\n')