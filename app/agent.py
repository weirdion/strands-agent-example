from aws_lambda_powertools import Logger
from strands import Agent
from tools import check_unraid_health

logger = Logger("strands-agent-example")

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[check_unraid_health],
    system_prompt=(
        "You are a helpful assistant, who is knowledgeable about various topics. "
        "Answer the user's questions to the best of your ability. "
        "You're tone should be friendly and informative. "
        "If you don't know the answer, say 'I don't know'. "
        "If the question is not clear, ask for clarification."
    ),
)


def invoke_agent(prompt: str) -> str:
    """
    Function to invoke the agent with a given prompt.
    """
    response = agent(prompt)
    logger.info(f"Agent response: {response}")
    return response.message
