from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: int  # reference to goal
    number: int  # task number within the goal
    name: str
    description: Optional[str] = None
    duration: Optional[int] = Field(default=None, description="Duration in minutes")
    priority: Optional[int] = Field(default=1, ge=1, le=5, description="Priority from 1 (lowest) to 5 (highest)")

class TaskCreate(SQLModel):
    name: str
    description: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[int] = Field(default=1, ge=1, le=5)

class TaskRead(SQLModel):
    id: int
    goal_id: int
    number: int
    name: str
    description: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[int]

class Goal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    current_task_number: int = 1  # pointer to current task; starts at 1

class GoalCreate(SQLModel):
    name: str
    description: Optional[str] = None

class GoalRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    current_task_number: int