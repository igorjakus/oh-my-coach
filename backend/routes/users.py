from enum import Enum
from fastapi import APIRouter, HTTPException
from typing import Optional

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
    Your tone is {tone.value}. Your motivation level is {motivation_level} out of 10.
    You focus on {task_focus.value} tasks. You communicate in {language.value}.
    Your response length is {response_length.value}.
    Your humor style is {humor_style.value}. Your empathy level is {empathy_level.value}.
    You reward users in a {reward_style.value} manner.
    You provide feedback in a {feedback_type.value} manner.
    """
    
    return prompt
