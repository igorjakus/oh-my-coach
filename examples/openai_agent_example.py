import os

from agents import Agent, Runner, set_default_openai_key
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(api_key)

agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant",
    model="gpt-4.1",
)

result = Runner.run_sync(
    agent, 
    "Write a haiku about recursion in programming.",
)

print(result.final_output)

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.