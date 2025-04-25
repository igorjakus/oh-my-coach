import asyncio
import os

from agents import ItemHelpers, MessageOutputItem, Runner, set_default_openai_key, trace
from dotenv import load_dotenv
from model_agents import (
    orchestrator_agent,
    synthesizer_agent,
)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
set_default_openai_key(api_key)

async def main():
    msg = input("Hi! What would you like translated, and to which languages? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = await Runner.run(orchestrator_agent, msg)

        for item in orchestrator_result.new_items:
            if isinstance(item, MessageOutputItem):
                text = ItemHelpers.text_message_output(item)
                if text:
                    print(f"  - Translation step: {text}")

        synthesizer_result = await Runner.run(synthesizer_agent, orchestrator_result.to_input_list())

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())