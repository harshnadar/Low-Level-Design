import threading
from typing import Callable
from queue import Queue, Empty
from src.scheduler.interfaces import IWorkerPool


class WorkerPool(IWorkerPool):
    """Thread pool for executing tasks"""
    
    def __init__(self, num_threads: int):
        self._num_threads = num_threads
        self._task_queue = Queue()
        self._workers = []
        self._shutdown_flag = threading.Event()
        self._initialize_workers()
    
    def _initialize_workers(self) -> None:
        """Create and start worker threads"""
        for i in range(self._num_threads):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"Worker-{i}",
                daemon=True
            )
            worker.start()
            self._workers.append(worker)
    
    def _worker_loop(self) -> None:
        """Main loop for worker threads"""
        while not self._shutdown_flag.is_set():
            try:
                task = self._task_queue.get(timeout=0.1)
                if task is not None:
                    try:
                        task()
                    except Exception as e:
                        print(f"Error in worker thread: {e}")
                    finally:
                        self._task_queue.task_done()
            except Empty:
                continue
    
    def submit_task(self, task: Callable[[], None]) -> None:
        """Submit a task to the worker pool"""
        if not self._shutdown_flag.is_set():
            self._task_queue.put(task)
    
    def shutdown(self) -> None:
        """Shutdown all worker threads"""
        self._shutdown_flag.set()
        
        # Add None tasks to wake up all workers
        for _ in range(self._num_threads):
            self._task_queue.put(None)
        
        # Wait for all workers to finish
        for worker in self._workers:
            worker.join(timeout=5.0)