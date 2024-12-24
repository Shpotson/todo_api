from datetime import datetime, timezone
import uuid
from pydantic import BaseModel
from enum import Enum

class TaskType(str, Enum):
    deadline = "deadline"
    event = "event"
    regular = "regular"

class Task(BaseModel):
    Name: str
    Id: str
    Type: TaskType
    Description: str
    CreatedAt: datetime
    UpdatedAt: datetime
    ToDate: datetime
    FromDate: datetime | None

    @staticmethod
    def create_new(
        name: str,
        task_type: TaskType,
        description: str,
        to_date: datetime,
        from_date: datetime | None):

        new_id = str(uuid.uuid4())
        utc_now = datetime.now(timezone.utc)

        task = Task(
            Id = new_id,
            Name=name,
            Type = task_type,
            Description = description,
            CreatedAt = utc_now,
            UpdatedAt = utc_now,
            ToDate = to_date,
            FromDate = from_date,
        )

        return task

    @staticmethod
    def create_from_db(
        task_id: str,
        name: str,
        task_type: TaskType,
        description: str,
        created_at: datetime,
        updated_at: datetime,
        to_date: datetime,
        from_date: datetime | None):

        task = Task(
            Id=task_id,
            Name=name,
            Type=task_type,
            Description=description,
            CreatedAt=created_at,
            UpdatedAt=updated_at,
            ToDate=to_date,
            FromDate=from_date,
        )

        return task

    def udpate(
        self,
        name: str,
        task_type: TaskType,
        description: str,
        to_date: datetime,
        from_date: datetime | None):

        self.Name = name
        self.Type = task_type
        self.Description = description
        self.ToDate = to_date
        self.FromDate = from_date


