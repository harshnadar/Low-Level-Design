from datetime import datetime, timedelta
from typing import Callable, Optional
from src.tasks.base_task import BaseTask


class RecurringTask(BaseTask):
    """Task that executes repeatedly at specified intervals"""
    
    def __init__(self, task_id: str, start_time: datetime, interval: timedelta, 
                 action: Callable[[], None], max_occurrences: Optional[int] = None):
        super().__init__(task_id, action)
        self._start_time = start_time
        self._interval = interval
        self._max_occurrences = max_occurrences
        self._occurrences = 0
        self._next_execution_time = start_time
    
    def get_next_execution_time(self) -> Optional[datetime]:
        """Calculate and return the next execution time"""
        if self._is_cancelled:
            return None
        
        if self._max_occurrences and self._occurrences >= self._max_occurrences:
            return None
        
        return self._next_execution_time
    
    def execute(self) -> None:
        """Execute the task and update next execution time"""
        if not self._is_cancelled:
            super().execute()
            self._occurrences += 1
            self._next_execution_time = self._next_execution_time + self._interval
    
    def is_recurring(self) -> bool:
        return True