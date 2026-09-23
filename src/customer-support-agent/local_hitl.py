"""Run the interactive handoff workflow with human input and tool approval."""

import asyncio
import os
from typing import Any

from agent_framework import AgentResponse, AgentResponseUpdate, Content
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import HandoffAgentUserRequest
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from observability import configure_local_observability
from workflow import build_customer_support_workflow


async def run() -> None:
    """Run the local HITL event loop."""
    load_dotenv()
    configure_local_observability()
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )
    workflow = build_customer_support_workflow(
        client,
        autonomous=False,
        require_tool_approval=True,
    )

    initial_message = input("Customer request: ").strip() or "I need help with an order."
    stream = workflow.run(initial_message, stream=True)

    while True:
        pending: list[Any] = []
        async for event in stream:
            if event.type == "request_info":
                pending.append(event)
            elif event.type == "handoff_sent":
                print(f"\nHandoff: {event.data.source} -> {event.data.target}")
            elif event.type == "output" and isinstance(event.data, AgentResponse):
                for message in event.data.messages:
                    if message.text:
                        print(f"{message.author_name or message.role}: {message.text}")
            elif event.type == "output" and not isinstance(event.data, (AgentResponse, AgentResponseUpdate)):
                print(f"\nCompleted: {event.data}")

        if not pending:
            return

        responses: dict[str, Any] = {}
        for request_event in pending:
            data = request_event.data
            if isinstance(data, HandoffAgentUserRequest):
                for message in data.agent_response.messages:
                    if message.text:
                        print(f"{message.author_name}: {message.text}")
                user_input = input("You: ").strip()
                if user_input.lower() in {"exit", "quit"}:
                    responses[request_event.request_id] = HandoffAgentUserRequest.terminate()
                else:
                    responses[request_event.request_id] = HandoffAgentUserRequest.create_response(user_input)
            elif isinstance(data, Content) and data.type == "function_approval_request":
                if data.function_call is None:
                    raise ValueError("Approval request is missing function call data.")
                print(f"Approval required: {data.function_call.name} {data.function_call.parse_arguments()}")
                approved = input("Approve this simulated action? [y/N]: ").strip().lower() == "y"
                responses[request_event.request_id] = data.to_function_approval_response(approved=approved)
            else:
                raise ValueError(f"Unsupported request type: {type(data)!r}")

        stream = workflow.run(responses=responses, stream=True)


if __name__ == "__main__":
    asyncio.run(run())

