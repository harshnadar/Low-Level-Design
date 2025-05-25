from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Optional
from src.scheduler.interfaces import ITask


class BaseTask(ITask, ABC):
    """Base implementation for all tasks"""
    
    def __init__(self, task_id: str, action: Callable[[], None]):
        self._task_id = task_id
        self._action = action
        self._is_cancelled = False
    
    def get_task_id(self) -> str:
        return self._task_id
    
    def execute(self) -> None:
        """Execute the task action if not cancelled"""
        if not self._is_cancelled:
            try:
                self._action()
            except Exception as e:
                print(f"Error executing task {self._task_id}: {e}")
    
    def cancel(self) -> None:
        """Cancel the task"""
        self._is_cancelled = True
    
    def is_cancelled(self) -> bool:
        """Check if task is cancelled"""
        return self._is_cancelled
    
    @abstractmethod
    def get_next_execution_time(self) -> Optional[datetime]:
        pass
    
    @abstractmethod
    def is_recurring(self) -> bool:
        pass