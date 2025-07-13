from dataclasses import dataclass
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from agent import invoke_agent

logger = Logger("strands-agent-example")
app = APIGatewayRestResolver(enable_validation=False)

@dataclass
class ResponseModel:
    message: str

    def to_dict(self) -> dict:
        return {
            "message": self.message
        }

@app.post("/invoke")
def call_agent(prompt: str) -> dict:
    """
    Example endpoint that simulates invoking an agent with a prompt.
    """
    logger.info(f"Received prompt: {prompt}")
    response = invoke_agent(prompt)
    logger.info(f"Response from agent: {response}")
    response_model = ResponseModel(message=response)
    return response_model.to_dict()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
