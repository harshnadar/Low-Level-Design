import unittest
from datetime import datetime, timedelta
from src.tasks.one_time_task import OneTimeTask
from src.tasks.recurring_task import RecurringTask


class TestTasks(unittest.TestCase):
    
    def test_one_time_task_properties(self):
        execution_time = datetime.now() + timedelta(hours=1)
        task = OneTimeTask(
            task_id="test_task",
            execution_time=execution_time,
            action=lambda: None
        )
        
        self.assertEqual(task.get_task_id(), "test_task")
        self.assertEqual(task.get_next_execution_time(), execution_time)
        self.assertFalse(task.is_recurring())
    
    def test_one_time_task_execution(self):
        counter = {'value': 0}
        
        def increment():
            counter['value'] += 1
        
        task = OneTimeTask(
            task_id="test_task",
            execution_time=datetime.now(),
            action=increment
        )
        
        # First execution should work
        task.execute()
        self.assertEqual(counter['value'], 1)
        
        # Second execution should not work (already executed)
        task.execute()
        self.assertEqual(counter['value'], 1)
        
        # Next execution time should be None after execution
        self.assertIsNone(task.get_next_execution_time())
    
    def test_recurring_task_properties(self):
        start_time = datetime.now() + timedelta(hours=1)
        interval = timedelta(minutes=30)
        
        task = RecurringTask(
            task_id="recurring_task",
            start_time=start_time,
            interval=interval,
            action=lambda: None
        )
        
        self.assertEqual(task.get_task_id(), "recurring_task")
        self.assertEqual(task.get_next_execution_time(), start_time)
        self.assertTrue(task.is_recurring())
    
    def test_recurring_task_execution(self):
        counter = {'value': 0}
        
        def increment():
            counter['value'] += 1
        
        start_time = datetime.now()
        interval = timedelta(seconds=1)
        
        task = RecurringTask(
            task_id="recurring_task",
            start_time=start_time,
            interval=interval,
            action=increment,
            max_occurrences=3
        )
        
        # Execute multiple times
        for i in range(5):
            if task.get_next_execution_time():
                task.execute()
        
        # Should only execute 3 times due to max_occurrences
        self.assertEqual(counter['value'], 3)
        self.assertIsNone(task.get_next_execution_time())
    
    def test_task_cancellation(self):
        counter = {'value': 0}
        
        def increment():
            counter['value'] += 1
        
        task = OneTimeTask(
            task_id="test_task",
            execution_time=datetime.now(),
            action=increment
        )
        
        # Cancel the task
        task.cancel()
        
        # Execution should not work after cancellation
        task.execute()
        self.assertEqual(counter['value'], 0)
        self.assertIsNone(task.get_next_execution_time())


if __name__ == '__main__':
    unittest.main()