from typing import Optional

from agents import Agent, set_default_openai_key
from pydantic import BaseModel

from backend.config import API_KEY

set_default_openai_key(API_KEY)

class AgentTask(BaseModel):
    name: str
    description: Optional[str]
    duration: Optional[int]
    priority: Optional[int]

goal_manager_agent = Agent(
    name="goal_manager_agent",
    instructions="""
    You are a goal generation expert that helps create goals.

    You should provide:
    - A clear, concise name
    - A short goal description
    - An estimated duration in minutes
    - A priority level [1, 5]
    """,
    output_type=AgentTask,
)