import asyncio
import os
from dataclasses import dataclass

from agents import Agent, Runner, WebSearchTool, function_tool, set_default_openai_key, trace
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(api_key)

client = OpenAI(api_key=api_key)


@dataclass
class Goal(BaseModel):
    title: str
    description: str
    duration: int
    priority: int


@dataclass
class Task(BaseModel):
    name: str
    description: str
    duration: int
    goal: str
    priority: int


@function_tool
def get_account_info(user_id: str) -> dict:
    """Return dummy account info for a given user."""
    return {
        "user_id": user_id,
        "name": "Bugs Bunny",
        "account_balance": "£72.50",
        "membership_status": "Gold Executive",
    }


def create_agent(name="", model="gpt-4.1", instructions="", tools=[], output_type=None):
    return Agent(name=name, model=model, instructions=(instructions), tools=tools, output_type=output_type)


friend_agent = create_agent(name="friend_agent", instructions="")
psychotherapist_agent = create_agent(name="psychotherapist_agent", instructions="")
physiotherapist_agent = create_agent(name="physiotherapist_agent", instructions="")
coach_agent = create_agent(name="coach_agent", instructions="")
motivator_agent = create_agent(name="motivator_agent", instructions="")
trainer_agent = create_agent(name="trainer_agent", instructions="")
dreamer_agent = create_agent(name="dreamer_agent", instructions="")
inspirer_agent = create_agent(name="inspirer_agent", instructions="")
nutritionist_agent = create_agent(name="nutritionist_agent", instructions="")
spiritualist_agent = create_agent(name="spiritualist_agent", instructions="")
financial_advisor_agent = create_agent(
    name="financial_advisor_agent", instructions=""
)  # TODO: raczej do wyrzucenia -> jest advisor
entertainer_agent = create_agent(name="entertainer_agent", instructions="")
task_manager_agent = create_agent(name="task_manager_agent", instructions="You provide tasks.", output_type=Task)
goal_manager_agent = create_agent(name="goal_manager_agent", instructions="")
listener_agent = create_agent(
    name="listener_agent", instructions=""
)  # brain dumper -> na koniec dnia i dostajesz jsona ładnie sparsowanego, tamten tylko słucha i się dopytuje czy coś jeszcze
versatile_agent = create_agent(
    name="versatile_agent", instructions="You speak weather."
)  # other things -> handluje wszystko inne, podtrzymanie rozmowy
expert_agent = create_agent(
    name="expert_agent",
    instructions="You immediately provide an input to the WebSearchTool to find up-to-date information on the user's query.",
    tools=[WebSearchTool()],
)
advisor_agent = create_agent(name="advisor_agent", instructions="You give advice for anything.")
task_validator_agent = create_agent(
    name="task_validator_agent", instructions=""
)  # TODO: może goal i task manager się tym będzie zajmować


triage_agent = Agent(
    name="Coach",
    instructions=prompt_with_handoff_instructions("""
You are the virtual coach. Welcome the user and ask how you can help.
Based on the user's intent, route to:
- versatile_agent for any unrealated queries, just continue the conversation
- advisor_agent for giving advices
- expert_agent for anything requiring real-time web search
- task_manager_agent for giving tasks
"""),
    handoffs=[
        friend_agent,
        psychotherapist_agent,
        physiotherapist_agent,
        coach_agent,
        motivator_agent,
        trainer_agent,
        dreamer_agent,
        inspirer_agent,
        nutritionist_agent,
        spiritualist_agent,
        financial_advisor_agent,
        entertainer_agent,
        task_manager_agent,
        goal_manager_agent,
        listener_agent,
        versatile_agent,
        expert_agent,
        advisor_agent,
        task_validator_agent,
    ],
)


async def test_queries():
    examples = [
        # "24342423?",  # versatile agent test
        # "Ooh i've got money to spend! What can I buy?",  # Advisor agent test
        # "Hmmm, what about duck hunting gear - what's trending right now?",  # Search Agent test
        "Give me tasks for learn AI",  # Task manager agent test
    ]

    with trace("Coach App"):
        for query in examples:
            result = await Runner.run(triage_agent, query)
            print(f"User: {query}")
            print(f"Answer: {result.final_output}")
            print("---")


asyncio.run(test_queries())
