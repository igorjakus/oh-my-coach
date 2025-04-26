from typing import Optional, Tuple

from agents import Agent, Runner, set_default_openai_key
from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from backend.config import API_KEY
from backend.models import Goal, PersonalisedAgent

set_default_openai_key(API_KEY)

class AgentGoal(BaseModel):
    """Output model for goal creation agent"""
    name: str
    description: Optional[str]

goal_manager_agent = Agent(
    name="goal_manager_agent",
    instructions="""
    You are a goal generation expert. You help users create goals based on their messages.
    Extract goal details from the user's message.
    
    You should provide:
    - A clear, concise name for the goal
    - A short description that explains what needs to be achieved
    
    Example:
    User: "I want to learn Python in next 3 months"
    Output:
    {
        "name": "Learn Python Programming",
        "description": "Master Python programming language fundamentals within a 3-month timeframe"
    }
    """,
    output_type=AgentGoal,
)

async def create_goal_from_prompt(user_prompt: str, session: Session) -> Goal:
    """
    Creates a new goal based on user's natural language prompt.
    
    Args:
        user_prompt: The user's message describing the goal
        session: Database session
        
    Returns:
        Goal: The created goal object
    """
    # Extract goal details using the agent
    result = await Runner.run(goal_manager_agent, f"Extract goal details from this message: {user_prompt}")
    
    if not isinstance(result.final_output, AgentGoal):
        raise HTTPException(
            status_code=500,
            detail="Failed to extract goal details from prompt"
        )
    
    # Create the goal in database
    db_goal = Goal(
        name=result.final_output.name,
        description=result.final_output.description,
        current_task_number=1
    )
    
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    
    return db_goal

async def create_goal_with_response(
    user_prompt: str,
    session: Session,
    personalised_agent_id: Optional[int] = None
) -> Tuple[Goal, str]:
    """
    Creates a goal and generates a personalized response about its creation.
    
    Args:
        user_prompt: The user's message describing the goal
        session: Database session
        personalised_agent_id: Optional ID of agent to personalize response
    Returns:
        Tuple[Goal, str]: The created goal object and response message
    """
    # Create the goal
    created_goal = await create_goal_from_prompt(user_prompt, session)
    
    # Generate base response
    response = f"OK, created new goal: '{created_goal.name}' (ID: {created_goal.id})."
    
    # Personalize if needed
    if personalised_agent_id:
        db_agent = session.get(PersonalisedAgent, personalised_agent_id)
        if db_agent:
            agent = Agent(name=db_agent.name, instructions=db_agent.prompt)
            result = await Runner.run(agent, f"Tell the user that a new goal has been created: {created_goal.name}")
            if result.final_output:
                response = result.final_output
                
    return created_goal, response