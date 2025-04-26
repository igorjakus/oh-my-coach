from typing import Optional, Tuple

from agents import Agent, Runner
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
from sqlmodel import Session, select

from backend.config import engine
from backend.models import Goal, Task, PersonalisedAgent


class AgentTask(BaseModel):
    """Output model for task creation agent"""
    name: str
    description: Optional[str]
    duration: Optional[int] = Field(description="Duration in minutes")
    priority: Optional[int] = Field(description="Priority from 1 (lowest) to 5 (highest)")

    @validator('priority')
    def validate_priority(cls, v):
        if v is not None and not (1 <= v <= 5):
            raise ValueError('Priority must be between 1 and 5')
        return v


task_manager_agent = Agent(
    name="task_manager_agent",
    instructions="""
    You are a task creation expert. You help create tasks based on user messages and goal context.
    
    You should provide:
    - A clear, concise task name
    - A short task description
    - Estimated duration in minutes (optional)
    - Priority level 1-5 (optional)
    
    The priority must be a number between 1 and 5, where:
    1 = lowest priority
    5 = highest priority
    
    Example:
    Goal: "Learn Python Programming"
    User: "I need to set up my development environment"
    Output:
    {
        "name": "Set up Python Development Environment",
        "description": "Install Python, configure IDE, and set up virtual environment",
        "duration": 60,
        "priority": 5
    }
    """,
    output_type=AgentTask,
)


async def create_task_from_prompt(goal_id: int, user_prompt: str, session: Session) -> Task:
    """
    Creates a new task based on user's natural language prompt.
    
    Args:
        goal_id: ID of the goal to create task for
        user_prompt: The user's message describing the task
        session: Database session
    Returns:
        Task: The created task object
    """
    # Get the goal first
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Get the context of previous tasks
    statement = select(Task).where(Task.goal_id == goal_id).order_by(Task.number)
    previous_tasks = session.exec(statement).all()
    
    # Build context for the agent
    context = f"""Goal: {goal.name}
Description: {goal.description}

Previous tasks:
{chr(10).join([f"- {task.name}: {task.description}" for task in previous_tasks]) if previous_tasks else "No previous tasks"}

User wants to create this task: {user_prompt}

Extract task details that fit this goal."""

    # Generate task details using the agent
    result = await Runner.run(task_manager_agent, context)
    
    if not isinstance(result.final_output, AgentTask):
        raise HTTPException(
            status_code=500,
            detail="Failed to extract task details from prompt"
        )
    
    # Determine the next task number
    next_number = (previous_tasks[-1].number + 1) if previous_tasks else 1
    
    # Create the task
    db_task = Task(
        goal_id=goal_id,
        number=next_number,
        name=result.final_output.name,
        description=result.final_output.description,
        duration=result.final_output.duration,
        priority=result.final_output.priority
    )
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task


async def generate_task(goal_id: int, previous_tasks: list[Task]) -> Task:
    """
    Generate a task based on the goal using task_manager_agent.
    Args:
        goal_id: ID of the goal to generate task for
        previous_tasks: List of previous tasks for context
    Returns:
        Task: Generated task with name, description, duration and priority
    """
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        context = f"Goal: {goal.name}\nDescription: {goal.description}\n"
        if previous_tasks:
            context += "\nPrevious tasks:\n" + "\n".join(
                [f"- {task.name}: {task.description}" for task in previous_tasks]
            )

        result = await Runner.run(task_manager_agent, f"Generate the next task for this goal: {context}")

        return result.final_output


async def create_task_with_response(
    goal_id: int,
    user_prompt: str,
    session: Session,
    personalised_agent_id: Optional[int] = None
) -> Tuple[Task, str]:
    """
    Creates a task and generates a personalized response about its creation.
    
    Args:
        goal_id: ID of the goal to create task for
        user_prompt: User's message describing the task
        session: Database session
        personalised_agent_id: Optional ID of agent to personalize response
    Returns:
        Tuple of (created task, response message)
    """
    # Create the task
    created_task = await create_task_from_prompt(goal_id, user_prompt, session)
    
    # Generate base response
    response = f"OK, added new task '{created_task.name}' to goal with ID {created_task.goal_id}."
    
    # Personalize if needed
    if personalised_agent_id:
        db_agent = session.get(PersonalisedAgent, personalised_agent_id)
        if db_agent:
            agent = Agent(name=db_agent.name, instructions=db_agent.prompt)
            result = await Runner.run(agent, f"Tell the user that a new task has been added: {created_task.name}")
            if result.final_output:
                response = result.final_output
                
    return created_task, response