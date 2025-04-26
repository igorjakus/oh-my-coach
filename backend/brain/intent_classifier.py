from agents import Agent, Runner
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from backend.config import engine
from backend.models import Goal


# Helper function to fetch existing goals from the database
def get_existing_goals():
    with Session(engine) as session:
        statement = select(Goal)
        goals = session.exec(statement).all()
        return goals

# Schema for task intent output: must contain goal_id as int where value is goal id or -1
class TaskIntentOutput(BaseModel):
    goal_id: int = Field(..., description="The goal ID associated with the task, or -1 if none")

# Schema for goal intent output: must contain is_new_goal as boolean true or false
class GoalIntentOutput(BaseModel):
    is_new_goal: bool = Field(..., description="True if message expresses intent to create new goal, else False")

# Creating an agent for classifying tasks for existing goals
task_intent_agent = Agent(
    name="Task Intent Classifier",
    instructions=(
        "You are a classifier that determines if a user's message is a task for an existing goal. "
        "Return a JSON object with a single integer field 'goal_id' which is the goal ID if the message is a task for one of the existing goals, otherwise -1."
    ),
    model="gpt-4.1",
    model_settings={"temperature": 0.0},  # deterministic output
)

# Creating an agent for classifying intent to create a new goal
goal_intent_agent = Agent(
    name="Goal Intent Classifier",
    instructions=(
        "You are a classifier that determines if a user's message expresses intent to create a new goal. "
        "Return a JSON object with a single boolean field 'is_new_goal' which is true if intent exists, otherwise false."
    ),
    model="gpt-4.1",
    model_settings={"temperature": 0.0},  # deterministic output
)

# Function to check if the message is a task for an existing goal
async def check_task_intent(message: str) -> int:
    goals = get_existing_goals()
    if not goals:
        return -1

    goals_context = "\n".join([
        f"Goal ID {goal.id}: {goal.name} - {goal.description}"
        for goal in goals
    ])

    completion = await Runner.run(
        task_intent_agent,
        f"Existing goals:\n{goals_context}\n\nUser message: {message}\n\nReturn the JSON object as specified.",
        text_format=TaskIntentOutput,
    )

    response = completion.final_output_parsed
    goal_id = response.goal_id

    # Validate if goal_id is in known goals or -1
    valid_goal_ids = [goal.id for goal in goals]
    if goal_id != -1 and goal_id not in valid_goal_ids:
        return -1

    return goal_id

# Function to check if the message expresses intent to create a new goal
async def check_goal_intent(message: str) -> bool:
    completion = await Runner.run(
        goal_intent_agent,
        f"User message: {message}\n\nReturn the JSON object as specified.",
        text_format=GoalIntentOutput,
    )

    response = completion.final_output_parsed
    return response.is_new_goal
