from typing import Optional

from agents import Agent, Runner
from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.config import engine
from backend.models import Goal, Task


class AgentTask(BaseModel):
    name: str
    description: Optional[str]
    duration: Optional[int]
    priority: Optional[int]

task_manager_agent = Agent(
    name="task_manager_agent",
    instructions="""You are a task generation expert that helps break down goals into simple tasks.

    For each task, you should provide:
    - A clear, concise name
    - A short task description
    - An estimated duration in minutes
    - A priority level [1, 5]

    Consider the context of previous tasks when generating new ones to ensure proper task sequencing.
    Apply pareto rule.""",
    output_type=AgentTask,
)

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