from agents import Agent, Runner
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from fastapi import HTTPException

from backend.brain.subagents import (
    coach_agent,
    dreamer_agent,
    entertainer_agent,
    expert_agent,
    friend_agent,
    motivator_agent,
    nutritionist_agent,
    physiotherapist_agent,
    psychotherapist_agent,
    trainer_agent,
    versatile_agent,
)

triage_agent = Agent(
    name="Coach",
    instructions=prompt_with_handoff_instructions("""You are the virtual coach. Welcome the user and ask how you can help.
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
    - task_manager_agent for generating tasks
    - goal_manager_agent for generating goals
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
        versatile_agent,
        expert_agent,
    ],
)

async def get_response_from_best_agent(query: str) -> str:
    """
    Get a response from the best agent based on the query.
    Args:
        query: User's query
    Returns:
        str: Response from the best agent
    """
    result = await Runner.run(triage_agent, query)
    if result.final_output:
        return result.final_output
    else:
        raise HTTPException(status_code=500, detail="No suitable agent found")

async def get_personalised_response(query: str, personalised_agent: Agent) -> str:
    """
    Get a response from the personalised agent based on the query.
    First gets response from best agent, then personalizes it.
    Args:
        query: User's query
        personalised_agent: Personalised agent to get response from
    Returns:
        str: Personalized response
    """
    # First get response from best agent
    base_response = await get_response_from_best_agent(query)
    
    # Then personalize the response
    prompt = f"""Original user query: {query}
Base response: {base_response}

Please rephrase this response in your personal style while maintaining the key information."""

    result = await Runner.run(personalised_agent, prompt)
    if result.final_output:
        return result.final_output
    else:
        # If personalization fails, return the base response
        return base_response