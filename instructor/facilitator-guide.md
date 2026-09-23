---
title: Facilitator guide
description: Timing, delivery guidance, demonstrations, checkpoints, and fallback options for workshop instructors
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: reference
estimated_reading_time: 10
---

## Delivery objective

Participants should leave with one coherent mental model:

```text
MAF defines agent behavior and orchestration.
Foundry hosts, identifies, observes, versions, and evaluates the agent.
Governance combines code policy, human decisions, identity, telemetry, and release gates.
```

## Timing plan

| Time      | Instructor action                           |
| --------- | ------------------------------------------- |
| 0:00-0:15 | Explain architecture and execution profiles |
| 0:15-0:45 | Guide the first local handoff               |
| 0:45-1:15 | Demonstrate approval and rejection          |
| 1:15-1:30 | Test routing policy and prompt injection    |
| 1:30-1:40 | Break and resolve environment issues        |
| 1:40-2:10 | Run local host, deploy, and invoke          |
| 2:10-2:30 | Inspect traces                              |
| 2:30-2:50 | Run evaluation and make a release decision  |
| 2:50-3:00 | Discuss durable HITL and summarize          |

## Instructor demonstrations

Prepare these demonstrations before participants arrive:

- Successful order lookup
- Approved return
- Rejected return
- Disallowed routing attempt
- Deployed hosted invocation
- Trace with at least one tool call
- Completed evaluation run

## Hard timeboxes

At 2:00, stop troubleshooting individual deployments. Move affected
participants to the shared instructor deployment.

At 2:30, use the precomputed evaluation run if participant evaluations are
still queued.

Do not extend the lab by asking participants to provision new projects or
implement durable hosted HITL.

## Teaching points

### MAF

Emphasize that MAF supplies agents, tools, workflow execution, handoff events,
and HITL request and response handling.

### Multi-agent design

Ask participants why one large agent with every tool is harder to govern.
Relate specialized agents to smaller permission and evaluation surfaces.

### HITL

Separate two concepts:

- A human provides conversational information.
- A human authorizes an action.

The second is the governance control.

### Foundry deployment

Explain that source-code deployment creates a managed, versioned endpoint.
The workshop uses an autonomous hosted profile to avoid teaching a misleading
in-memory approval pattern.

### Observability

Start with a question, not a trace tour:

```text
Why did the return tool run?
```

Use the trace to reconstruct routing, prompts, model calls, and tool
arguments.

### Governance

Toolkit features support investigation. The release decision still depends on
documented thresholds, identity controls, and an accountable owner.

## Fallback assets

Keep these available:

- A known-good `.env`
- One active hosted version
- Trace IDs for three workshop scenarios
- One completed evaluation run
- A screen recording of deployment
- A zipped `.venv` only when classroom networking is unreliable

Never distribute credentials or a committed `.env`.

## Production extension

Use the final ten minutes to sketch durable HITL:

```text
request_info event
    -> persist workflow checkpoint
    -> create approval record
    -> notify authorized reviewer
    -> receive correlated decision
    -> restore checkpoint
    -> execute idempotent tool
```

Point participants to the MAF checkpoint and HITL documentation for further
study.
