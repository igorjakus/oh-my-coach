from typing import Optional

from agents import Agent
from fastapi import HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session

from backend.brain.goal_creator import create_goal_with_response
from backend.brain.intent_classifier import check_goal_intent, check_task_intent
from backend.brain.task_creator import create_task_with_response
from backend.brain.triage import get_personalised_response, get_response_from_best_agent
from backend.config import engine
from backend.models import PersonalisedAgent


class ProcessedMessageResponse(BaseModel):
    """Output model for processed message"""
    response: str
    intent_type: str = Field(
        default="general_chat",
        description="Type of detected intent. Can be: create_task, create_goal, general_chat"
    )
    entity_id: Optional[int] = Field(
        default=None,
        description="ID of created entity (task or goal) if applicable"
    )


async def handle_general_chat(
    query: str,
    personalised_agent_id: Optional[int] = None,
    session: Session = None
) -> str:
    """Handle general chat using triage or personalized agent."""
    if personalised_agent_id:
        db_agent = session.get(PersonalisedAgent, personalised_agent_id)
        if not db_agent:
            raise HTTPException(status_code=404, detail="Personalised agent not found")
        
        agent = Agent(name=db_agent.name, instructions=db_agent.prompt)
        return await get_personalised_response(query, agent)
    
    return await get_response_from_best_agent(query)


async def process_message(
    query: str,
    personalised_agent_id: Optional[int] = None,
    session: Session = None
) -> ProcessedMessageResponse:
    """
    Process a user message through the complete pipeline:
    1. Check if it's a task for an existing goal
    2. Check if it's a new goal
    3. Fall back to standard triage
    """
    if session is None:
        session = Session(engine)
        
    try:
        # Step 1: Check for task creation intent
        task_intent = await check_task_intent(query)
        if task_intent != -1:  # -1 means no task intent
            created_task, response = await create_task_with_response(
                task_intent,
                query,
                session,
                personalised_agent_id
            )
            return ProcessedMessageResponse(
                response=response,
                intent_type="create_task",
                entity_id=created_task.id
            )
        
        # Step 2: Check for goal creation intent
        if await check_goal_intent(query):
            created_goal, response = await create_goal_with_response(
                query,
                session,
                personalised_agent_id
            )
            return ProcessedMessageResponse(
                response=response,
                intent_type="create_goal",
                entity_id=created_goal.id
            )
        
        # Step 3: Handle general chat
        response = await handle_general_chat(query, personalised_agent_id, session)
        return ProcessedMessageResponse(
            response=response,
            intent_type="general_chat"
        )
            
    except Exception as e:
        print(f"Error in process_message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )
    finally:
        if session is not None:
            session.close()