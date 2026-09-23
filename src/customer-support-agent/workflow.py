"""Build the customer-support handoff workflow."""

from agent_framework import Agent
from agent_framework.orchestrations import HandoffBuilder

from support_tools import get_order_status, process_return, process_return_autonomous


def build_customer_support_workflow(client, *, autonomous: bool, require_tool_approval: bool):
    """Create a constrained triage, order, and return handoff workflow."""
    triage_agent = Agent(
        client=client,
        name="triage_agent",
        instructions=(
            "You are a customer-support triage agent. Identify the user's intent and hand off immediately. "
            "Use order_agent for order status and return_agent for returns. Never perform specialist work. "
            "When a specialist has resolved the request, ask whether the user needs anything else. "
            "If the request is complete and no more input is needed, say 'Goodbye!' to end the workflow."
        ),
    )

    order_agent = Agent(
        client=client,
        name="order_agent",
        instructions=(
            "You handle order status questions. Ask for a three-digit order number if it is missing. "
            "Use get_order_status, summarize the result, and hand control back to triage_agent."
        ),
        tools=[get_order_status],
    )

    return_tool = process_return if require_tool_approval else process_return_autonomous
    return_agent = Agent(
        client=client,
        name="return_agent",
        instructions=(
            "You handle refunds and replacements. Collect the three-digit order number and whether the customer "
            "wants a refund or replacement. Call the available return-processing tool only after both values are "
            "known. Explain that the workshop tool is a simulation, then hand control back to triage_agent."
        ),
        tools=[return_tool],
    )

    builder = (
        HandoffBuilder(
            name="governed_customer_support",
            participants=[triage_agent, order_agent, return_agent],
            termination_condition=lambda conversation: (
                len(conversation) > 0 and "goodbye" in conversation[-1].text.lower()
            ),
        )
        .with_start_agent(triage_agent)
        .add_handoff(triage_agent, [order_agent, return_agent])
        .add_handoff(order_agent, [triage_agent, return_agent])
        .add_handoff(return_agent, [triage_agent])
    )

    if autonomous:
        builder = builder.with_autonomous_mode()

    return builder.build()

