import json

from aws_lambda_powertools import Logger
from strands import tool
from strands.types.tools import ToolResult, ToolResultContent

logger = Logger("strands-agent-example")


@tool(name="check_unraid_health", description="Check the health of the unraid system")
def check_unraid_health() -> ToolResult:
    """
    Function to check the health of the unraid system.
    """
    # Mock call via VPC endpoint to check health of my unraid system at home.
    response = ToolResult(
        toolUseId="unraid-health-check-12345",
        status="success",
        content=[
            ToolResultContent(
                text=json.dumps(
                    [
                        {
                            "drive": "Disk 1",
                            "status": "operational",
                            "temperature": "30C",
                            "errors": 0,
                        },
                        {
                            "drive": "Disk 2",
                            "status": "operational",
                            "temperature": "35C",
                            "errors": 30,
                        },
                    ]
                )
            )
        ],
    )
    logger.info(f"Unraid health check response: {response}")
    return response
