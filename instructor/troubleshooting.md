---
title: Workshop troubleshooting
description: Fast recovery guidance for authentication, model, deployment, trace, and evaluation failures
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: troubleshooting
estimated_reading_time: 8
---

## Authentication fails

Check:

```bash
az account show
azd auth status
```

Participants must complete interactive authentication themselves.

## The project endpoint is rejected

Use the project endpoint, not the account endpoint:

```text
https://<account>.services.ai.azure.com/api/projects/<project>
```

Confirm `FOUNDRY_PROJECT_ENDPOINT` in the agent `.env`.

## The model cannot be found

Confirm that `AZURE_AI_MODEL_DEPLOYMENT_NAME` is a deployment name in the
selected project. A catalog model name is not sufficient.

## Agent Inspector cannot connect

Check ports:

```bash
curl http://localhost:8088/health
```

Stop the previous debugging task before starting another server.

## Local HITL produces no approval event

Confirm that `local_hitl.py` builds the workflow with:

```python
require_tool_approval=True
```

Confirm that the return agent actually attempts to call `process_return`.

## Deployment builds but invocation fails

Compare local and deployed configuration:

```bash
azd env get-values
azd ai agent show --output json
```

Check the hosted-agent logs and verify runtime identity access to the model.

## Traces do not appear

Verify:

- Application Insights is connected to the Foundry project
- The hosted invocation succeeded
- The selected time range covers the invocation
- The participant has Log Analytics Reader

Trace ingestion can be delayed.

## Prompt and response content is missing

Content capture is disabled by default. Enable it only for approved synthetic
workshop data:

```text
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT="true"
```

## Evaluation commands differ

The CLI experience is in preview. Run:

```bash
azd ai agent eval --help
```

Follow the syntax reported by the installed extension. Use the instructor's
saved evaluation run if the service is unavailable.

## Deployment is taking too long

At the workshop timebox, switch the participant to the shared instructor
deployment. Continue with traces and evaluation rather than waiting.
