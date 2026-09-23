---
title: Instructor environment setup checklist
description: Pre-provisioning and validation checklist for reliable workshop delivery
author: Workshop maintainers
ms.date: 2026-09-23
ms.topic: reference
estimated_reading_time: 6
---

## Two weeks before delivery

- [ ] Confirm a supported Foundry region
- [ ] Confirm model availability and quota
- [ ] Create or select the workshop Foundry project
- [ ] Deploy the workshop chat model
- [ ] Connect Application Insights
- [ ] Confirm hosted-agent source-code deployment is available
- [ ] Decide whether participants use individual or shared projects

## One week before delivery

- [ ] Assign Foundry Project Manager for deployers
- [ ] Assign Foundry User
- [ ] Assign Log Analytics Reader on Application Insights
- [ ] Confirm classroom or conference network access
- [ ] Test GitHub Codespaces or the dev container
- [ ] Run `./scripts/validate.sh` in the dev container
- [ ] Deploy the instructor agent
- [ ] Generate representative traces
- [ ] Run and save the smoke evaluation

## One day before delivery

- [ ] Recheck quota and project health
- [ ] Recheck role assignments with a participant account
- [ ] Verify `azd` and Foundry extension versions
- [ ] Verify the model deployment name
- [ ] Verify the project endpoint
- [ ] Test the Agent Inspector launch configuration
- [ ] Test local interactive HITL
- [ ] Test remote invocation
- [ ] Confirm traces appear
- [ ] Confirm evaluation results are accessible

## Before participants begin

Provide:

- Repository URL
- Project endpoint
- Project Azure resource ID
- Model deployment name
- Azure tenant and subscription IDs
- Authentication instructions
- Shared fallback agent name
- Support channel

Do not provide:

- API keys
- Connection strings
- Personal `.env` files
- Subscription owner credentials

## Cleanup decision

Document whether the environment is:

- Retained for continued learning
- Shared with another workshop
- Deleted after the event

Do not run `azd down` against a shared project. Delete only resources that the
workshop environment owns.
