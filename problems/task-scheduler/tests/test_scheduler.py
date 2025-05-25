import unittest
import time
from datetime import datetime, timedelta
from src.scheduler.task_scheduler import TaskScheduler
from src.tasks.one_time_task import OneTimeTask
from src.tasks.recurring_task import RecurringTask


class TestTaskScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = TaskScheduler(num_threads=2)
    
    def tearDown(self):
        self.scheduler.shutdown()
    
    def test_one_time_task_execution(self):
        counter = {'value': 0}
        
        def increment():
            counter['value'] += 1
        
        task = OneTimeTask(
            task_id="test_one_time",
            execution_time=datetime.now() + timedelta(seconds=1),
            action=increment
        )
        
        self.scheduler.schedule_task(task)
        time.sleep(2)
        
        self.assertEqual(counter['value'], 1)
    
    def test_recurring_task_execution(self):
        counter = {'value': 0}
        
        def increment():
            counter['value'] += 1
        
        task = RecurringTask(
            task_id="test_recurring",
            start_time=datetime.now() + timedelta(seconds=1),
            interval=timedelta(seconds=1),
            action=increment
        )
        
        self.scheduler.schedule_task(task)
        time.sleep(3.5)
        
        self.assertGreaterEqual(counter['value'], 2)
        self.assertLessEqual(counter['value'], 4)
    
    def test_task_priority_ordering(self):
        execution_order = []
        
        def create_action(task_id):
            def action():
                execution_order.append(task_id)
            return action
        
        now = datetime.now()
        
        # Schedule tasks in reverse order
        task3 = OneTimeTask("task3", now + timedelta(seconds=3), create_action("task3"))
        task1 = OneTimeTask("task1", now + timedelta(seconds=1), create_action("task1"))
        task2 = OneTimeTask("task2", now + timedelta(seconds=2), create_action("task2"))
        
        self.scheduler.schedule_task(task3)
        self.scheduler.schedule_task(task1)
        self.scheduler.schedule_task(task2)
        
        time.sleep(4)
        
        self.assertEqual(execution_order, ["task1", "task2", "task3"])


if __name__ == '__main__':
    unittest.main()