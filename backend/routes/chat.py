from fastapi import APIRouter, Depends
from openai import OpenAI
from pydantic import BaseModel
from sqlmodel import Session

from backend.brain import ProcessedMessageResponse, process_message
from backend.config import API_KEY, engine

chat_router = APIRouter()
client = OpenAI(api_key=API_KEY)

def get_session():
    with Session(engine) as session:
        yield session

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    prompt: str
    history: list[Message] = []


@chat_router.post("/", response_model=ProcessedMessageResponse)
async def get_personalised_response(
    agent_id: int,
    request: ChatRequest,
    session: Session = Depends(get_session)
) -> ProcessedMessageResponse:
    """
    Process message through the complete pipeline with personalization.
    """
    return await process_message(
        query=request.prompt,
        personalised_agent_id=agent_id,
        session=session
    )
