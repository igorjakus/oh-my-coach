from enum import Enum

from agents import Agent
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.config import engine
from backend.models import PersonalisedAgent

personalization_router = APIRouter()


# ========== SESSION ==========
def get_session():
    with Session(engine) as session:
        yield session


# ========== ENUMS ==============
class Tone(Enum):
    FRIENDLY = "friendly"
    FORMAL = "formal"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    SERIOUS = "serious"

class TaskFocus(Enum):
    PRODUCTIVITY = "productivity"
    HEALTH = "health"
    LEARNING = "learning"
    DAILY_HABITS = "daily_habits"

class Language(Enum):
    PL = "pl"
    EN = "en"

class ResponseLength(Enum):
    SHORT = "short"
    DETAILED = "detailed"
    FLEXIBLE = "flexible"

class HumorStyle(Enum):
    NONE = "none"
    DAD_JOKES = "dad_jokes"
    IRONIC = "ironic"
    LIGHT = "light"

class EmpathyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RewardStyle(Enum):
    ENTHUSIASTIC = "enthusiastic"
    MODERATE = "moderate"
    CREATIVE = "creative"

class FeedbackType(Enum):
    POSITIVE = "positive"
    CONSTRUCTIVE = "constructive"
    HONEST = "honest"


# ========== ENDPOINTS ==============
def create_agent_prompt(
    pseudonym: str,
    personality: str,
    tone: Tone,
    motivation_level: int,
    task_focus: TaskFocus,
    language: Language,
    response_length: ResponseLength = ResponseLength.FLEXIBLE,
    humor_style: HumorStyle = HumorStyle.NONE,
    empathy_level: EmpathyLevel = EmpathyLevel.MEDIUM,
    reward_style: RewardStyle = RewardStyle.MODERATE,
    feedback_type: FeedbackType = FeedbackType.CONSTRUCTIVE,
) -> str:
    """
    Create a personalized agent prompt based on user preferences.
    """
    if not 1 <= motivation_level <= 10:
        raise ValueError("motivation_level must be between 1 and 10.")

    prompt = f"""
    You are a personal assistant named {pseudonym}. Your personality is {personality}.
    Your tone is {tone.value}. Your motivational intensity is {motivation_level}/10 
    (where 1 means gentle encouragement and 10 means intense drill sergeant style motivation).
    You focus on {task_focus.value} tasks. You communicate in {language.value}.
    Your response length is {response_length.value}.
    Your humor style is {humor_style.value}. Your empathy level is {empathy_level.value}.
    You reward users in a {reward_style.value} manner.
    You provide feedback in a {feedback_type.value} manner.
    """
    
    return prompt


@personalization_router.post("/create_agent")
async def create_personalized_agent(
    pseudonym: str,
    personality: str,
    tone: Tone,
    motivation_level: int,
    task_focus: TaskFocus,
    language: Language,
    response_length: ResponseLength = ResponseLength.FLEXIBLE,
    humor_style: HumorStyle = HumorStyle.NONE,
    empathy_level: EmpathyLevel = EmpathyLevel.MEDIUM,
    reward_style: RewardStyle = RewardStyle.MODERATE,
    feedback_type: FeedbackType = FeedbackType.CONSTRUCTIVE,
    session: Session = Depends(get_session)
):
    """
    Create a personalized agent based on user preferences and store it in the database.
    """
    try:
        prompt = create_agent_prompt(
            pseudonym,
            personality,
            tone,
            motivation_level,
            task_focus,
            language,
            response_length,
            humor_style,
            empathy_level,
            reward_style,
            feedback_type
        )
        
        # Store the prompt and name in the database
        db_agent = PersonalisedAgent(name=pseudonym, prompt=prompt)
        session.add(db_agent)
        session.commit()
        session.refresh(db_agent)
        
        # Create and return the agent with stored prompt
        return {
            "id": db_agent.id,
            "name": db_agent.name,
            "agent": Agent(
                name=pseudonym,
                instructions=prompt,
            )
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the agent: {str(e)}")

@personalization_router.get("/agent/{agent_id}")
async def get_agent(agent_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a personalized agent from the database by ID.
    """
    db_agent = session.get(PersonalisedAgent, agent_id)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@personalization_router.get("/agents", response_model=list[PersonalisedAgent])
async def get_all_agents(session: Session = Depends(get_session)):
    """
    Retrieve all personalized agents from the database.
    """
    statement = select(PersonalisedAgent)
    agents = session.exec(statement).all()
    return agents

@personalization_router.delete("/agent/{agent_id}")
async def delete_agent(agent_id: int, session: Session = Depends(get_session)):
    """
    Delete a personalized agent from the database by ID.
    """
    db_agent = session.get(PersonalisedAgent, agent_id)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    session.delete(db_agent)
    session.commit()
    
    return {"detail": "Agent deleted successfully"}
