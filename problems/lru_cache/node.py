class Node:
    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev = None
        self.next = None