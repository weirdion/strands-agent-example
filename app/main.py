from dataclasses import dataclass

from agent import invoke_agent
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.parser import BaseModel, ValidationError
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import Field

logger = Logger("strands-agent-example")
app = APIGatewayRestResolver(enable_validation=True)


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
def call_agent() -> dict:
    """
    Example endpoint that simulates invoking an agent with a prompt.
    """
    try:
        request_body = app.current_event.json_body

        if not request_body:
            logger.warning("Empty request body received")
            error_response = ErrorResponseModel(
                error="missing_body", message="Request body is required"
            )
            raise BadRequestError(error_response.to_dict())

        prompt = request_body.get("prompt")
        if prompt is None or not isinstance(prompt, str) or not prompt.strip():
            logger.warning("Empty or invalid prompt received")
            error_response = ErrorResponseModel(
                error="invalid_prompt", message="The 'prompt' field must be a non-empty string"
            )
            raise BadRequestError(error_response.to_dict())

        logger.info(f"Received prompt: {prompt}")
        response = invoke_agent(prompt.strip())
        logger.info(f"Response from agent: {response}")

        response_model = ResponseModel(message=response)
        return response_model.to_dict()
    except Exception as e:
        logger.error(f"Unexpected error processing request: {e}")
        error_response = ErrorResponseModel(
            error="internal_error",
            message="An unexpected error occurred while processing your request",
        )
        raise BadRequestError(error_response.to_dict())


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
