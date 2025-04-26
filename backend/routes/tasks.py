from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, delete, select

from backend.brain import generate_task
from backend.config import engine
from backend.models import Goal, GoalCreate, GoalRead, Task, TaskCreate, TaskRead

task_router = APIRouter()


# ========== SESSION ==========
def get_session():
    with Session(engine) as session:
        yield session


# ========== ENDPOINTS ==============
# ========== GET ENDPOINTS ==========
@task_router.get("/goals", response_model=List[GoalRead])
async def get_all_goals(session: Session = Depends(get_session)):
    """Get all goals from the database"""
    statement = select(Goal)
    goals = session.exec(statement).all()
    return goals


@task_router.get("/tasks/{task_id}", response_model=TaskRead)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    # Read task by ID
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.get("/goals/{goal_id}/current-task", response_model=TaskRead)
async def get_current_task(goal_id: int, session: Session = Depends(get_session)):
    """Get the current task for a goal based on current_task_number"""
    # Get the goal
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Get the current task
    current_task = session.exec(
        select(Task)
        .where(Task.goal_id == goal_id, Task.number == goal.current_task_number)
        .limit(1)
    ).first()
    
    if not current_task:
        raise HTTPException(status_code=404, detail="No current task found")
    
    return current_task

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


# =========== POST ENDPOINTS ==========
@task_router.post("/goals", response_model=GoalRead)
async def create_goal(goal: GoalCreate, session: Session = Depends(get_session)):
    # Create a new goal
    db_goal = Goal(**goal.dict())
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal

@task_router.post("/goals/{goal_id}/next-task", response_model=TaskRead)
async def go_to_next_task(goal_id: int, session: Session = Depends(get_session)):
    """Move to the next task and return that task"""
    # Get the goal
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Get all tasks to check if we have a next one
    statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number)
    tasks = session.exec(statement).all()
    if goal.current_task_number >= len(tasks):
        raise HTTPException(status_code=400, detail="No next task")
    
    # Get the next task
    next_task = session.exec(
        select(Task)
        .where(Task.goal_id == goal_id, Task.number == goal.current_task_number)
        .limit(1)
    ).first()
    if not next_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Advance the pointer
    goal.current_task_number += 1
    session.add(goal)
    session.commit()
    
    return next_task

@task_router.post("/goals/{goal_id}/generate-task", response_model=TaskRead)
async def generate_and_create_task(goal_id: int, session: Session = Depends(get_session)):
    """Generate a new task using AI and add it to the goal"""
    # Get the goal first to check current_task_number
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Get only tasks up to current_task_number for context
    statement = select(Task).where(
        Task.goal_id == goal_id,
    ).order_by(Task.number)
    previous_tasks = session.exec(statement).all()
    
    # Generate new task using AI
    generated_task = await generate_task(goal_id, previous_tasks)
    
    # Get the highest task number to determine next number
    max_number_statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number.desc())
    last_task = session.exec(max_number_statement).first()
    next_number = (last_task.number + 1) if last_task else 1
    
    # Create task in database
    db_task = Task(
        goal_id=goal_id,
        number=next_number,
        name=generated_task.name,
        description=generated_task.description,
        duration=generated_task.duration,
        priority=generated_task.priority
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@task_router.post("/goals/{goal_id}/tasks", response_model=TaskRead)
async def create_task_manually(goal_id: int, task: TaskCreate, session: Session = Depends(get_session)):
    # Add a new task at the end (max number + 1)
    statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number.desc())
    last_task = session.exec(statement).first()
    next_number = (last_task.number + 1) if last_task else 1
    db_task = Task(goal_id=goal_id, number=next_number, **task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


# ==== DELETE ENDPOINTS ====
@task_router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: int, session: Session = Depends(get_session)):
    # Delete goal and all its tasks
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # First delete all associated tasks
    statement = delete(Task).where(Task.goal_id == goal_id)
    session.exec(statement)
    
    # Then delete the goal
    session.delete(goal)
    session.commit()
    return {"ok": True}
