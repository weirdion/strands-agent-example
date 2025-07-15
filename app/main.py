from dataclasses import dataclass

from agent import invoke_agent
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.parser import parse as powertools_parse
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel

logger = Logger("strands-agent-example")
app = APIGatewayRestResolver(enable_validation=True)


class PromptModel(BaseModel):
    prompt: str


@dataclass
class ResponseModel:
    message: str

    def to_dict(self) -> dict:
        return {"message": self.message}


@dataclass
class ErrorResponseModel:
    error: str
    message: str

    def to_dict(self) -> dict:
        return {"error": self.error, "message": self.message}


@app.post("/invoke")
def call_agent(prompt_model: PromptModel) -> dict:
    """
    Example endpoint that simulates invoking an agent with a prompt.
    """
    prompt = prompt_model.prompt
    logger.info(f"Received prompt: {prompt}")

    try:
        if not prompt.strip():
            raise BadRequestError("Prompt cannot be empty.")
        response = invoke_agent(prompt.strip())
        logger.info(f"Response from agent: {response}")

    except BadRequestError as e:
        logger.error(f"Bad request error: {e}")
        error_response = ErrorResponseModel(error="BadRequest", message=str(e))
        return error_response.to_dict()
    except Exception as e:
        logger.error(f"Error invoking agent: {e}")
        error_response = ErrorResponseModel(error="AgentInvocationError", message=str(e))
        return error_response.to_dict()

    response_model = ResponseModel(message=response)
    return response_model.to_dict()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext) -> dict:
    parsed_event = powertools_parse(event=event, model=APIGatewayProxyEventModel)
    return app.resolve(parsed_event, context)
