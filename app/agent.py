from aws_lambda_powertools import Logger
from strands import Agent

logger = Logger("strands-agent-example")

agent = Agent(model="us.anthropic.claude-3-7-sonnet-20250219-v1:0")


def invoke_agent(prompt: str) -> str:
    """
    Function to invoke the agent with a given prompt.
    """
    response = agent(prompt)
    logger.info(f"Agent response: {response}")
    return response.message
