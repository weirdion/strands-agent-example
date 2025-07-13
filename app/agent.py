from aws_lambda_powertools import Logger
from strands import Agent

logger = Logger("strands-agent-example")

agent = Agent()

def invoke_agent(prompt: str) -> str:
    """
    Function to invoke the agent with a given prompt.
    """
    logger.info("Invoking agent with prompt: ", agent.model.config)
    logger.info(f"Invoking agent with prompt: {prompt}")
    response = agent.invoke(prompt)
    logger.info(f"Agent response: {response}")
    return response

