from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, Optional


class ITask(ABC):
    """Interface for all tasks"""
    
    @abstractmethod
    def get_task_id(self) -> str:
        """Get the unique identifier of the task"""
        pass
    
    @abstractmethod
    def get_next_execution_time(self) -> Optional[datetime]:
        """Get the next execution time for the task"""
        pass
    
    @abstractmethod
    def execute(self) -> None:
        """Execute the task action"""
        pass
    
    @abstractmethod
    def is_recurring(self) -> bool:
        """Check if the task is recurring"""
        pass


class ITaskScheduler(ABC):
    """Interface for task scheduler"""
    
    @abstractmethod
    def schedule_task(self, task: ITask) -> None:
        """Schedule a task for execution"""
        pass
    
    @abstractmethod
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task"""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the scheduler and all worker threads"""
        pass


class IWorkerPool(ABC):
    """Interface for worker pool management"""
    
    @abstractmethod
    def submit_task(self, task: Callable[[], None]) -> None:
        """Submit a task to the worker pool"""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown all worker threads"""
        pass