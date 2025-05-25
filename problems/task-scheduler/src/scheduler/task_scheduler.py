import threading
from datetime import datetime
import time
from typing import Dict, Optional
from src.scheduler.interfaces import ITaskScheduler, ITask
from src.scheduler.worker_pool import WorkerPool
from src.utils.priority_queue import PriorityQueue


class TaskScheduler(ITaskScheduler):
    """Main task scheduler implementation"""
    
    def __init__(self, num_threads: int = 4):
        self._worker_pool = WorkerPool(num_threads)
        self._task_queue = PriorityQueue[ITask]()
        self._active_tasks: Dict[str, ITask] = {}
        self._scheduler_thread = None
        self._shutdown_flag = threading.Event()
        self._lock = threading.Lock()
        self._start_scheduler()
    
    def _start_scheduler(self) -> None:
        """Start the scheduler thread"""
        self._scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            name="Scheduler-Thread",
            daemon=True
        )
        self._scheduler_thread.start()
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop that checks for tasks to execute"""
        while not self._shutdown_flag.is_set():
            try:
                current_time = datetime.now()
                
                # Process all tasks that are ready
                while True:
                    next_task_info = self._task_queue.peek()
                    
                    if next_task_info:
                        execution_time, task = next_task_info
                        
                        if execution_time <= current_time:
                            # Remove task from queue
                            result = self._task_queue.get(timeout=0.01)
                            if result:
                                _, task = result
                                # Submit task for execution
                                self._worker_pool.submit_task(lambda t=task: self._execute_task(t))
                        else:
                            # No more tasks ready, calculate sleep time
                            sleep_time = min((execution_time - current_time).total_seconds(), 0.1)
                            time.sleep(max(0.001, sleep_time))
                            break
                    else:
                        # No tasks in queue
                        time.sleep(0.01)
                        break
                    
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                import traceback
                traceback.print_exc()
    
    def _execute_task(self, task: ITask) -> None:
        """Execute a task and reschedule if recurring"""
        try:
            task.execute()
            
            # If task is recurring, reschedule it
            if task.is_recurring():
                next_time = task.get_next_execution_time()
                if next_time:
                    self._task_queue.put(next_time, task, task.get_task_id())
                else:
                    # Task completed all occurrences
                    with self._lock:
                        self._active_tasks.pop(task.get_task_id(), None)
            else:
                # One-time task completed
                with self._lock:
                    self._active_tasks.pop(task.get_task_id(), None)
                    
        except Exception as e:
            print(f"Error executing task {task.get_task_id()}: {e}")
            import traceback
            traceback.print_exc()
    
    def schedule_task(self, task: ITask) -> None:
        """Schedule a task for execution"""
        with self._lock:
            task_id = task.get_task_id()
            
            # Cancel existing task with same ID if any
            if task_id in self._active_tasks:
                self.cancel_task(task_id)
            
            # Add task to active tasks
            self._active_tasks[task_id] = task
            
            # Get next execution time and add to queue
            next_time = task.get_next_execution_time()
            if next_time:
                self._task_queue.put(next_time, task, task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a scheduled task"""
        with self._lock:
            if task_id in self._active_tasks:
                task = self._active_tasks[task_id]
                if hasattr(task, 'cancel'):
                    task.cancel()
                
                # Remove from queue
                self._task_queue.remove(task_id)
                
                # Remove from active tasks
                del self._active_tasks[task_id]
                return True
            return False
    
    def shutdown(self) -> None:
        """Shutdown the scheduler and all worker threads"""
        self._shutdown_flag.set()
        
        # Wait for scheduler thread to finish
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5.0)
        
        # Shutdown worker pool
        self._worker_pool.shutdown()