from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

from backend.config import API_KEY

chat_router = APIRouter()
client = OpenAI(api_key=API_KEY)

class ChatRequest(BaseModel):
    prompt: str
    history: list[str] = []

@chat_router.post("/", response_model=str)
def get_completion(request: ChatRequest) -> str:
    """
    Get a completion from the OpenAI API.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1", messages=[{"role": "user", "content": request.prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
