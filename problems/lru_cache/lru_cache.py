from node import Node
from typing import Any
from threading import Lock

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.lock = Lock()

    def get(self, key: Any) -> int: 
        with self.lock: #acquire lock for reading
            if key in self.cache:
                node = self.cache[key]
                self._move_to_head(node)
                return node.value
            return None
    
    def put(self, key: Any, value: Any) -> None:
        with self.lock:
            if key in self.cache:
                node = self.cache[key]
                node.value = value
                self._move_to_head(node)
            else:
                node = Node(key, value)
                self.cache[key] = node
                self._add_to_head(node)
                if len(self.cache) > self.capacity:
                    #remove the least recently used item
                    tail = self.tail.prev
                    self._remove(tail)
                    del self.cache[tail.key]
    
    def _add_to_head(self, node: Node) -> None:
        #add the node to the head of the doubly linked list
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove(self, node: Node) -> None:
        #remove the node from the doubly linked list
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _move_to_head(self, node: Node) -> None:
        #if the node is already the head, do nothing
        if node.next is None:
            return
        #remove the node from its current position
        self._remove(node)
        #add the node to the head
        self._add_to_head(node)
        
