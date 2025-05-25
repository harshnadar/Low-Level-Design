from datetime import datetime, timedelta
import time
from src.scheduler.task_scheduler import TaskScheduler
from src.tasks.one_time_task import OneTimeTask
from src.tasks.recurring_task import RecurringTask


def main():
    """Example usage of the task scheduler"""
    
    # Create scheduler with 3 worker threads
    scheduler = TaskScheduler(num_threads=3)
    
    # Example 1: One-time task
    def print_message(msg):
        def action():
            print(f"[{datetime.now()}] {msg}")
        return action
    
    # Schedule a one-time task
    one_time_task = OneTimeTask(
        task_id="greeting",
        execution_time=datetime.now() + timedelta(seconds=2),
        action=print_message("Hello from one-time task!")
    )
    scheduler.schedule_task(one_time_task)
    
    # Example 2: Recurring task
    counter = {'value': 0}
    
    def increment_counter():
        counter['value'] += 1
        print(f"[{datetime.now()}] Counter: {counter['value']}")
    
    recurring_task = RecurringTask(
        task_id="counter",
        start_time=datetime.now() + timedelta(seconds=1),
        interval=timedelta(seconds=1),
        action=increment_counter,
        max_occurrences=5
    )
    scheduler.schedule_task(recurring_task)
    
    # Example 3: Multiple tasks with priorities
    for i in range(3):
        task = OneTimeTask(
            task_id=f"priority_task_{i}",
            execution_time=datetime.now() + timedelta(seconds=3+i),
            action=print_message(f"Priority task {i}")
        )
        scheduler.schedule_task(task)
    
    # Let tasks run
    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        scheduler.shutdown()
        print("Scheduler stopped.")


if __name__ == "__main__":
    main()