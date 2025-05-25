from datetime import datetime
from typing import Callable, Optional
from src.tasks.base_task import BaseTask


class OneTimeTask(BaseTask):
    """Task that executes only once at a specified time"""
    
    def __init__(self, task_id: str, execution_time: datetime, action: Callable[[], None]):
        super().__init__(task_id, action)
        self._execution_time = execution_time
        self._executed = False
    
    def get_next_execution_time(self) -> Optional[datetime]:
        """Return execution time if not yet executed, None otherwise"""
        if self._executed or self._is_cancelled:
            return None
        return self._execution_time
    
    def execute(self) -> None:
        """Execute the task and mark as executed"""
        if not self._executed and not self._is_cancelled:
            super().execute()
            self._executed = True
    
    def is_recurring(self) -> bool:
        return False