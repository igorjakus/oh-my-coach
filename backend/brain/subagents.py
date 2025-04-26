from agents import Agent, WebSearchTool, set_default_openai_key
from openai import OpenAI

from backend.config import API_KEY

set_default_openai_key(API_KEY)
client = OpenAI(api_key=API_KEY)

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
    instructions="You are dealing with user who doesn't have any goal set in their life. Give propositions of such goals that are suitable to the user.",
)
nutritionist_agent = create_agent(
    name="nutritionist_agent",
    instructions="You are a nutritionist. Based on user's story give some eating advice.",
)
entertainer_agent = create_agent(
    name="entertainer_agent",
    instructions="You are supposed to entertain the user. You can do this by recommending movies, books, games ect. based on their story.",
)
versatile_agent = create_agent(
    name="versatile_agent", instructions="You are trying to keep the conversation with the user flowing."
)
expert_agent = create_agent(
    name="expert_agent",
    instructions="You immediately provide an input to the WebSearchTool to find up-to-date information on the user's query.",
    tools=[WebSearchTool()],
)