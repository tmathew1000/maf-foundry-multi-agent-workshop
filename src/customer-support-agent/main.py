"""Serve the autonomous workshop workflow through the Foundry Responses protocol."""

import os

from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from workflow import build_customer_support_workflow


def main() -> None:
    """Start the hosted-agent server."""
    load_dotenv()
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )
    workflow_agent = build_customer_support_workflow(
        client,
        autonomous=True,
        require_tool_approval=False,
    ).as_agent()
    ResponsesHostServer(workflow_agent).run()


if __name__ == "__main__":
    main()
