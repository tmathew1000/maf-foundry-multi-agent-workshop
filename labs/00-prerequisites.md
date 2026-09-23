---
title: Prepare your workshop environment
description: Verify the tools, access, model, and local configuration required for the workshop
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: tutorial
estimated_reading_time: 8
---

## Goal

Prepare a consistent Python 3.13 development environment and verify access to
the Foundry project supplied by your instructor.

Allow 15 minutes before the scheduled workshop or complete these steps as
pre-work.

## Required access

Your instructor provides:

- A Microsoft Foundry project endpoint
- The Foundry project Azure resource ID
- A deployed chat model name
- The Azure tenant and subscription IDs
- Foundry Project Manager access for hosted-agent deployment
- Foundry User access
- Log Analytics Reader access for the connected Application Insights resource

> [!IMPORTANT]
> Do not create a new project or model deployment during the workshop unless
> your instructor explicitly directs you to do so.

## Recommended environment

Use GitHub Codespaces or the repository dev container. It includes:

- Python 3.13
- Azure CLI
- Azure Developer CLI
- GitHub CLI
- Recommended VS Code extensions

Open the repository in the dev container and wait for the dependency setup to
finish.

## Authenticate

Run the following commands yourself:

```bash
az login
azd auth login
```

Confirm both sessions:

```bash
az account show --query "{subscription:name, tenant:tenantId}" --output table
azd auth status
```

Install or update the Foundry extension when needed:

```bash
azd ext install microsoft.foundry
```

## Configure the local agent

Move into the agent project:

```bash
cd src/customer-support-agent
```

Create the local environment file:

```bash
cp .env.example .env
```

Set these values in `.env`:

```text
FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
AZURE_AI_MODEL_DEPLOYMENT_NAME="<deployment-name>"
ENABLE_LOCAL_TRACING="false"
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="false"
```

Keep the project resource ID, tenant ID, and subscription ID available for
Lab 3. Do not add them to the source `.env`.

Synchronize the environment:

```bash
uv sync
```

## Verify your setup

Run the deterministic unit test:

```bash
uv run pytest
```

Expected result:

```text
1 passed
```

Run a syntax and lint check:

```bash
uv run ruff check .
uv run python -m compileall -q .
```

## Completion checkpoint

You are ready when:

- Azure CLI and Azure Developer CLI are authenticated
- The `.env` file contains the instructor-provided project values
- `uv sync` completes
- The test and lint checks pass

Continue to [Explore the MAF multi-agent workflow](01-multi-agent.md).
