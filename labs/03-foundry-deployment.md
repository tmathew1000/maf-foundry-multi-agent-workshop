---
title: Deploy the hosted agent to Foundry
description: Run the autonomous Responses profile locally and deploy the Python source to Foundry Agent Service
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: tutorial
estimated_reading_time: 12
---

## Goal

Expose the workflow through the Responses protocol and deploy it as a Foundry
hosted agent.

Allow 30 minutes.

## Compare execution profiles

| Profile    | Entry point     | Behavior                                 |
| ---------- | --------------- | ---------------------------------------- |
| Local HITL | `local_hitl.py` | Interactive handoffs and approval events |
| Hosted     | `main.py`       | Autonomous handoffs in one invocation    |

The hosted tool is still a simulation, but it does not pause for approval.
This keeps the deployment exercise compatible with a single Responses API
invocation.

## Review the hosting layer

Open `src/customer-support-agent/main.py`.

The entry point:

1. Creates a `FoundryChatClient`.
2. Builds the autonomous handoff workflow.
3. Converts the workflow to an agent with `.as_agent()`.
4. Starts `ResponsesHostServer`.

Open `azure.yaml` and locate:

- Python 3.13 runtime
- Source-code deployment configuration
- Responses protocol version
- Agent project path
- Model deployment dependency

## Run with Agent Inspector

Press `F5` and select:

```text
Debug Local Agent/Workflow HTTP Server
```

Foundry Toolkit starts the workflow server and opens Agent Inspector.

Send a complete prompt:

```text
Return order 456 for a replacement. Complete the simulated request and finish the conversation.
```

> [!TIP]
> The hosted autonomous profile needs a complete request. It cannot pause to
> ask a person for missing details.

## Verify the Foundry environment

From the repository root, create an `azd` environment. Add your initials to
the environment name so it is unique:

```bash
azd env new workshop-<initials>
```

Bind the environment to the instructor-provided project:

```bash
azd env set AZURE_AI_PROJECT_ENDPOINT "<project-endpoint>"
azd env set AZURE_AI_PROJECT_ID "<project-resource-id>"
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "<deployment-name>"
azd env set AZURE_SUBSCRIPTION_ID "<subscription-id>"
azd env set AZURE_TENANT_ID "<tenant-id>"
```

Verify the selected values:

```bash
azd env get-values
azd ai project show --output json
azd ai agent show --output json
```

Ask your instructor for help if the configured project is not the workshop
project. A not-deployed agent status is expected before the first deployment.

## Deploy the source

Run:

```bash
azd deploy customer-support-agent
```

Foundry packages the source, resolves Python dependencies remotely, and creates
an immutable agent version.

## Invoke the deployed version

Run:

```bash
azd ai agent invoke "Where is order 123? Complete the simulated request and finish the conversation."
```

You can also use the agent playground link printed by the deployment command.

## Completion checkpoint

You have completed this lab when:

- The hosted version reports an active status
- A remote invocation returns a response
- The response identifies the correct specialist behavior
- You can locate the deployed version in Foundry

Continue to
[Trace, evaluate, and govern the release](04-observability-governance.md).
