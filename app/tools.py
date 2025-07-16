import json

from aws_lambda_powertools import Logger
from strands import tool

logger = Logger("strands-agent-example")


@tool(name="check_unraid_health", description="Check the health of the unraid system")
def check_unraid_health() -> str:
    """
    Function to check the health of the unraid system.
    """
    # Mock call via VPC endpoint to check health of my unraid system at home.
    response = {
        "status": "success",
        "content": [
            {
                "drive": "Disk 1",
                "status": "operational",
                "temperature": "30C",
                "errors": 0,
            },
            {
                "drive": "Disk 2",
                "status": "operational",
                "temperature": "32C",
                "errors": 0,
            },
        ],
    }
    logger.info(f"Unraid health check response: {response}")
    return response
