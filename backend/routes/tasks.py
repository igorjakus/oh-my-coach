from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, select

from backend.config import engine

task_router = APIRouter()


# ===== MODELS =====
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_id: int  # reference to goal
    number: int  # task number within the goal
    name: str
    description: Optional[str] = None

class TaskCreate(SQLModel):
    name: str
    description: Optional[str] = None

class TaskRead(SQLModel):
    id: int
    goal_id: int
    number: int
    name: str
    description: Optional[str] = None

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


# ========== SESSION ==========
def get_session():
    with Session(engine) as session:
        yield session


# ========== ENDPOINTS ==========
@task_router.post("/goals", response_model=GoalRead)
async def create_goal(goal: GoalCreate, session: Session = Depends(get_session)):
    # Create a new goal
    db_goal = Goal(**goal.dict())
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal

@task_router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: int, session: Session = Depends(get_session)):
    # Delete goal and all its tasks
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    session.delete(goal)
    session.exec(select(Task).where(Task.goal_id == goal_id)).delete()
    session.commit()
    return {"ok": True}

@task_router.post("/goals/{goal_id}/tasks", response_model=TaskRead)
async def create_task(goal_id: int, task: TaskCreate, session: Session = Depends(get_session)):
    # Add a new task at the end (max number + 1)
    statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number.desc())
    last_task = session.exec(statement).first()
    next_number = (last_task.number + 1) if last_task else 1
    db_task = Task(goal_id=goal_id, number=next_number, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@task_router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    # Read task by ID
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.post("/goals/{goal_id}/next-task", response_model=GoalRead)
async def go_to_next_task(goal_id: int, session: Session = Depends(get_session)):
    # Move to the next task (advance current_task_number)
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    statement = select(Task).where(Task.goal_id == goal_id)
    max_number = session.exec(statement).all()
    if goal.current_task_number >= len(max_number):
        raise HTTPException(status_code=400, detail="No next task")
    goal.current_task_number += 1
    session.add(goal)
    session.commit()
    return goal

@task_router.get("/goals/{goal_id}/done-tasks", response_model=List[TaskRead])
async def get_done_tasks(goal_id: int, session: Session = Depends(get_session)):
    # Get done tasks (numbers less than current)
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    statement = select(Task).where(
        Task.goal_id == goal_id,
        Task.number < goal.current_task_number
    ).order_by(Task.number)
    done_tasks = session.exec(statement).all()
    return done_tasks

@task_router.get("/goals/{goal_id}/tasks", response_model=List[TaskRead])
async def get_all_goal_tasks(goal_id: int, session: Session = Depends(get_session)):
    # Get all tasks for the goal
    statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number)
    tasks = session.exec(statement).all()
    return tasks
