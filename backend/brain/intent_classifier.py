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
        "Analyze the message and the list of existing goals. "
        "If the message is clearly about creating a task for one of the listed goals, return that goal's ID. "
        "Otherwise return -1. "
        "Your response must be a JSON object with a single field 'goal_id' containing this integer."
    ),
    output_type=TaskIntentOutput
)

# Creating an agent for classifying intent to create a new goal
goal_intent_agent = Agent(
    name="Goal Intent Classifier",
    instructions=(
        "You are a classifier that determines if a user's message expresses intent to create a new goal. "
        "Return a JSON object with a single boolean field 'is_new_goal' which is true if intent exists, otherwise false."
    ),
    output_type=GoalIntentOutput
)

async def check_task_intent(message: str) -> int:
    """
    Checks if the message is intended to be a task for an existing goal.
    Returns the goal ID if it is, -1 otherwise.
    """
    goals = get_existing_goals()
    if not goals:
        return -1

    goals_context = "\n".join([
        f"Goal ID {goal.id}: {goal.name} - {goal.description}"
        for goal in goals
    ])

    try:
        result = await Runner.run(
            task_intent_agent,
            f"""Analyze if this message is meant to create a task for one of these goals:

{goals_context}

User message: "{message}"

Return the goal_id if this is clearly a task for that goal, or -1 if not."""
        )

        if hasattr(result, 'final_output') and isinstance(result.final_output, TaskIntentOutput):
            goal_id = result.final_output.goal_id
            # Validate if goal_id exists
            if goal_id != -1 and goal_id in [goal.id for goal in goals]:
                return goal_id
    except Exception as e:
        print(f"Error in check_task_intent: {str(e)}")
    
    return -1

async def check_goal_intent(message: str) -> bool:
    """
    Checks if the message expresses intent to create a new goal.
    Returns True if it does, False otherwise.
    """
    try:
        result = await Runner.run(
            goal_intent_agent,
            f"""Determine if this message expresses an intent to create a new goal:

User message: "{message}"

Return is_new_goal=true only if this clearly indicates wanting to create a new goal."""
        )

        if hasattr(result, 'final_output') and isinstance(result.final_output, GoalIntentOutput):
            return result.final_output.is_new_goal
    except Exception as e:
        print(f"Error in check_goal_intent: {str(e)}")
    
    return False
