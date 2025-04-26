import asyncio
import os
from typing import Optional

from agents import Agent, Runner, WebSearchTool, set_default_openai_key, trace
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI
from pydantic import BaseModel
from sqlmodel import Session

from backend.config import engine
from backend.models import Goal, Task

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(api_key)

client = OpenAI(api_key=api_key)


def create_agent(name="", model="gpt-4.1", instructions="", tools=[], output_type=None):
    return Agent(name=name, model=model, instructions=(instructions), tools=tools, output_type=output_type)


friend_agent = create_agent(
    name="friend_agent", instructions="You are a user's friend listening to the story and asking follow-up questions."
)
psychotherapist_agent = create_agent(
    name="psychotherapist_agent",
    instructions="You are a psychotherapist. You should listen to user's queries, explain why they feel the way they feel and give advise.",
)
physiotherapist_agent = create_agent(
    name="physiotherapist_agent",
    instructions="You are a physiotherapist. You should listen to user's queries, explain their problem based on symptoms and suggest exercises.",
)
coach_agent = create_agent(
    name="coach_agent",
    instructions="You are user's personal coach. You listen to user's queries and give general advice in their situation.",
)
motivator_agent = create_agent(
    name="motivator_agent",
    instructions="You are user's motivator. You encourage them, for example by pointing out benefits of the goal set.",
)
trainer_agent = create_agent(
    name="trainer_agent",
    instructions="You are user's personal trainer. You should ask about their weight, age ect. and propose adequate exercises for achieving their goal.",
)
dreamer_agent = create_agent(
    name="dreamer_agent",
    instructions="You are dealing with user who doesn't have any goal set in their life. Give propositions of such goals that are suitable to the user, maybe by asking additional questions.",
)
nutritionist_agent = create_agent(
    name="nutritionist_agent",
    instructions="You are a nutritionist. Based on user's story give some eating advice, maybe by asking additional questions.",
)
entertainer_agent = create_agent(
    name="entertainer_agent",
    instructions="You are supposed to entertain the user. You can do this by recommending movies, books, games ect. based on their story, maybe by asking additional questions.",
)

# Define a simplified Task model for the agent without defaults
class AgentTask(BaseModel):
    name: str
    description: Optional[str]
    duration: Optional[int]
    priority: Optional[int]


task_manager_agent = create_agent(
    name="task_manager_agent", 
    instructions="""You are a task generation expert that helps break down goals into actionable tasks. 
    For each task, you should provide:
    - A clear, concise name
    - A detailed description explaining what needs to be done
    - An estimated duration in minutes
    - A priority level from 1 (lowest) to 5 (highest) based on task importance
    
    Consider the context of previous tasks when generating new ones to ensure proper task sequencing.
    Tasks should be concrete, measurable, and help directly progress towards the goal.""", 
    output_type=AgentTask
)
goal_manager_agent = create_agent(name="goal_manager_agent", instructions="You are giving goals.", output_type=Goal)

versatile_agent = create_agent(
    name="versatile_agent", instructions="You are trying to keep the conversation with the user flowing."
)
expert_agent = create_agent(
    name="expert_agent",
    instructions="You immediately provide an input to the WebSearchTool to find up-to-date information on the user's query.",
    tools=[WebSearchTool()],
)

triage_agent = Agent(
    name="Coach",
    instructions=prompt_with_handoff_instructions("""
You are the virtual coach. Welcome the user and ask how you can help.
Based on the user's intent, route to:
- friend_agent for friendly conversations
- psychotherapist_agent for mental health advice
- physiotherapist_agent for physical health advice
- coach_agent for general advice
- motivator_agent for motivating
- trainer_agent for fitness advice
- dreamer_agent for goal suggestions
- nutritionist_agent for eating advice
- entertainer_agent for entertainment generation
- task_manager_agent for managing tasks
- goal_manager_agent for managing goals
- expert_agent for anything requiring real-time web search
- versatile_agent for any unrelated queries, just continue the conversation
"""),
    handoffs=[
        friend_agent,
        psychotherapist_agent,
        physiotherapist_agent,
        coach_agent,
        motivator_agent,
        trainer_agent,
        dreamer_agent,
        nutritionist_agent,
        entertainer_agent,
        task_manager_agent,
        goal_manager_agent,
        versatile_agent,
        expert_agent,
    ],
)



async def generate_task(goal_id: int, previous_tasks: list[Task]) -> Task:
    """
    Generate a task based on the goal using task_manager_agent.
    Args:
        goal_id: ID of the goal to generate task for
        previous_tasks: List of previous tasks for context
    Returns:
        Task: Generated task with name, description, duration and priority
    """
    with Session(engine) as session:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        context = f"Goal: {goal.name}\nDescription: {goal.description}\n"
        if previous_tasks:
            context += "\nPrevious tasks:\n" + "\n".join([f"- {task.name}: {task.description}" for task in previous_tasks])
        
        result = await Runner.run(
            task_manager_agent,
            f"Generate the next task for this goal: {context}"
        )
        
        return result.final_output  # task_manager_agent will return Task object since we set output_type=Task


async def test_queries():
    examples = [
        # "24342423?",  # versatile agent test
        "Ooh i've got money to spend! What can I buy?",  # Advisor agent test
        # "Hmmm, what about duck hunting gear - what's trending right now?",  # Search Agent test
    ]

    with trace("Coach App"):
        for query in examples:
            result = await Runner.run(triage_agent, query)
            print(f"User: {query}")
            print(f"Answer: {result.final_output}")
            print("---")


if __name__ == "__main__":
    asyncio.run(test_queries())