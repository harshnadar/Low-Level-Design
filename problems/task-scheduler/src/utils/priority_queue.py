import heapq
from typing import Generic, TypeVar, Tuple, Optional, List
from datetime import datetime
import threading
import time

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    """Thread-safe priority queue implementation"""
    
    def __init__(self):
        self._queue: List[List] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._task_entry_map = {}  # Map task_id to entry
        self._counter = 0  # Tie-breaker for items with same priority
    
    def put(self, priority: datetime, item: T, task_id: str) -> None:
        """Add an item with priority (earlier time = higher priority)"""
        with self._lock:
            # If task already exists, mark it as cancelled
            if task_id in self._task_entry_map:
                old_entry = self._task_entry_map[task_id]
                old_entry[3] = True  # Mark as cancelled
            
            # Add new entry [priority, counter, item, cancelled, task_id]
            entry = [priority, self._counter, item, False, task_id]
            self._counter += 1
            self._task_entry_map[task_id] = entry
            heapq.heappush(self._queue, entry)
            self._condition.notify()
    
    def get(self, timeout: Optional[float] = None) -> Optional[Tuple[datetime, T]]:
        """Get the highest priority item (earliest time)"""
        with self._lock:
            end_time = None
            if timeout is not None:
                end_time = time.time() + timeout
            
            while True:
                # Remove any cancelled entries from the top
                while self._queue and self._queue[0][3]:  # Check cancelled flag
                    entry = heapq.heappop(self._queue)
                    task_id = entry[4]
                    if task_id in self._task_entry_map and self._task_entry_map[task_id] is entry:
                        del self._task_entry_map[task_id]
                
                if self._queue:
                    entry = heapq.heappop(self._queue)
                    priority, _, item, cancelled, task_id = entry
                    if not cancelled:
                        if task_id in self._task_entry_map and self._task_entry_map[task_id] is entry:
                            del self._task_entry_map[task_id]
                        return priority, item
                
                # Calculate remaining timeout
                if timeout is None:
                    wait_time = None
                else:
                    if end_time is None:
                        return None
                    wait_time = end_time - time.time()
                    if wait_time <= 0:
                        return None
                
                # Wait for new items
                if not self._condition.wait(wait_time):
                    return None
    
    def peek(self) -> Optional[Tuple[datetime, T]]:
        """Peek at the highest priority item without removing it"""
        with self._lock:
            # Skip cancelled entries
            while self._queue and self._queue[0][3]:
                entry = heapq.heappop(self._queue)
                task_id = entry[4]
                if task_id in self._task_entry_map and self._task_entry_map[task_id] is entry:
                    del self._task_entry_map[task_id]
            
            if self._queue:
                return self._queue[0][0], self._queue[0][2]
            return None
    
    def remove(self, task_id: str) -> bool:
        """Remove a task by its ID"""
        with self._lock:
            if task_id in self._task_entry_map:
                entry = self._task_entry_map[task_id]
                entry[3] = True  # Mark as cancelled
                del self._task_entry_map[task_id]
                self._condition.notify()
                return True
            return False
    
    def empty(self) -> bool:
        """Check if queue is empty"""
        with self._lock:
            # Clean up cancelled entries
            while self._queue and self._queue[0][3]:
                entry = heapq.heappop(self._queue)
                task_id = entry[4]
                if task_id in self._task_entry_map and self._task_entry_map[task_id] is entry:
                    del self._task_entry_map[task_id]
            return len(self._queue) == 0