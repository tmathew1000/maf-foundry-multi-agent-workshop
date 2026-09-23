"""Deterministic tools used by the customer-support agents."""

from typing import Annotated

from agent_framework import tool
from pydantic import Field


def _return_confirmation(order_number: str, return_type: str) -> str:
    confirmation = f"RET-{order_number}-{return_type.upper()}"
    return (
        f"Simulated return for order {order_number}: {return_type} approved. "
        f"Confirmation: {confirmation}. No external system was changed."
    )


@tool
def get_order_status(
    order_number: Annotated[str, Field(description="The three-digit order number.")],
) -> dict[str, str]:
    """Return deterministic sample status data for an order."""
    return {
        "order_number": order_number,
        "status": "In transit",
        "estimated_delivery": "Friday",
    }


@tool(approval_mode="always_require")
def process_return(
    order_number: Annotated[str, Field(description="The three-digit order number.")],
    return_type: Annotated[str, Field(description="Either refund or replacement.")],
) -> str:
    """Simulate a return after explicit human approval."""
    return _return_confirmation(order_number, return_type)


@tool(approval_mode="never_require")
def process_return_autonomous(
    order_number: Annotated[str, Field(description="The three-digit order number.")],
    return_type: Annotated[str, Field(description="Either refund or replacement.")],
) -> str:
    """Simulate a return in the hosted autonomous demonstration."""
    return _return_confirmation(order_number, return_type)
