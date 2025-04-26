from agents import Agent
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from backend.brain import get_best_response, get_response_from_best_agent
from backend.config import API_KEY

chat_router = APIRouter()
client = OpenAI(api_key=API_KEY)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    prompt: str
    history: list[Message] = []


@chat_router.post("/", response_model=str)
async def get_completion(request: ChatRequest) -> str:
    """
    Get a completion from the OpenAI API using conversation history.
    """
    try:
        # Convert history to the format expected by OpenAI
        messages = [{"role": msg.role, "content": msg.content} for msg in request.history]
        # Add the current user message
        messages.append({"role": "user", "content": request.prompt})
        
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/triage", response_model=str)
async def get_triage_response(request: ChatRequest) -> str:
    query = "".join([msg.content for msg in request.history]) + request.prompt
    return await get_response_from_best_agent(query)


@chat_router.post("/personalised", response_model=str)
async def get_personalised_response(request: ChatRequest, personalised_agent) -> str:
    """
    Get a personalised response from the best agent based on the query.
    """    
    query = "".join([msg.content for msg in request.history]) + request.prompt
    return await get_best_response(query, personalised_agent)
