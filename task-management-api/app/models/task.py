import app.utils.constants as constants
import datetime
import uuid

class Task:
    def __init__(self, title, description, task_status: str = constants.TaskStatus.PENDING, task_priority: str = constants.TaskPriority.MEDIUM):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.task_status = task_status
        self.task_priority = task_priority
        self.created_at = datetime.datetime.now()
        self.last_updated = datetime.datetime.now()

    # def change_priority(self, new_priority: str):
    #     self.task_priority = new_priority

    # def change_status(self, new_status: str):
    #     self.task_status = new_status

    # def last_updated(self):
    #     self.last_updated = datetime.datetime.now()

    def get_task_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "task_status": str(self.task_status),
            "task_priority": str(self.task_priority),
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }

    def __repr__(self):
        return f"<Task(title={self.title}, completed={self.completed})>"