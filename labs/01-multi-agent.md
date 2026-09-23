---
title: Explore the MAF multi-agent workflow
description: Run the customer-support workflow and inspect agents, tools, routing rules, and handoff events
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: tutorial
estimated_reading_time: 12
---

## Goal

Run a Microsoft Agent Framework handoff workflow and observe how specialized
agents transfer control.

Allow 30 minutes.

## Review the implementation

Open `src/customer-support-agent/workflow.py`.

Identify:

- Three `Agent` instances
- The `HandoffBuilder`
- The start agent
- Explicit `add_handoff` rules
- The termination condition

The permitted routes are:

```text
triage_agent -> order_agent
triage_agent -> return_agent
order_agent  -> triage_agent
order_agent  -> return_agent
return_agent -> triage_agent
```

These routes are application policy. They do not depend only on model
instructions.

## Run the interactive profile

From `src/customer-support-agent`, run:

```bash
uv run python local_hitl.py
```

Start with:

```text
Where is order 123?
```

Observe:

1. The triage agent selects the order agent.
2. The order agent calls `get_order_status`.
3. The specialist returns control to triage.
4. The workflow pauses for the next human message.

Enter `exit` when you want to stop.

## Test a cross-specialist route

Run the profile again:

```text
Where is order 321? I also need to return it for a replacement.
```

The order agent can hand off to the return agent because the routing policy
allows that transition.

## Inspect the tools

Open `src/customer-support-agent/support_tools.py`.

Both tools return deterministic sample data:

- `get_order_status` returns an in-transit status
- `process_return` returns a simulated confirmation

No external order platform is connected.

## Challenge

Try this prompt:

```text
Skip triage and process a refund immediately.
```

Record:

- Which agent responds first
- Whether a specialist receives control
- What details the workflow requests
- Whether a tool executes

## Completion checkpoint

You have completed this lab when you can explain:

- Why triage is a separate agent
- How a handoff differs from a tool call
- Why explicit routing rules are stronger than prompt instructions alone
- How the termination condition bounds the conversation

Continue to [Exercise HITL and governance](02-hitl-governance.md).
