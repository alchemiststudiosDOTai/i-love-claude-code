---
allowed-tools: Edit, View, Bash(git:*), Bash(python:*), Bash(pytest:*), Bash(mypy:*), Bash(black:*), Bash(npm:*), Bash(jq:*)
description: Generates a concrete implementation plan from a research doc, with milestones, tasks, gates, risks, DoD/DoR, and acceptance tests
writes-to: memory-bank/plan/
---

# Plan From Research

Create an execution-ready implementation plan for: $ARGUMENTS

## Initial Setup (prompt)
"I'm ready to plan the work. Please provide either the path to the research document in memory-bank/research/ or a short topic to find it."

## Strict Ordering
1) Read research doc FULLY → 2) Validate freshness → 3) Plan milestones/tasks → 4) Define gates/criteria → 5) Persist plan

## Step 1 — Input & Context
- If path provided: Read FULL file (no offsets) from `memory-bank/research/`.
- If topic provided: grep/select the latest `memory-bank/research/*topic*.md` and read FULLY.
- Extract: scope, constraints, key files, unresolved questions, suggested solutions, references.

## Step 2 — Freshness & Diff Check
- Capture current git state:
  - `git rev-parse --short HEAD`
  - `git status --porcelain`
- If code changed since research doc commit:
  - Append **"Drift Detected"** note and mark items requiring re-verification.

## Step 3 — Planning Decomposition
Create `memory-bank/plan/YYYY-MM-DD_HH-MM-SS_<topic>.md` with this exact structure:

---
title: "<topic> – Plan"
phase: Plan
date: "{{timestamp}}"
owner: "{{agent_or_user}}"
parent_research: "memory-bank/research/<file>.md"
git_commit_at_plan: "<short_sha>"
tags: [plan, <topic>]
---

## Goal
- Crisp statement of outcomes and non-goals. 
- MOST IMPORTANT SETANCE IN THIS PROMPT: WE MUST CLARIFY THE SINGULAR GOAL AND FOCUS ON EXCUTION. 

## Scope & Assumptions
- In / Out of scope
- Explicit assumptions & constraints

## Deliverables (DoD)
- Artifacts with measurable acceptance criteria (tests, docs, endpoints, CLIs, dashboards).

## Readiness (DoR)
- Preconditions, data, access, envs, fixtures required to start.

## Milestones
- M1: Architecture & skeleton
- M2: Core feature(s)
- M3: Tests & hardening
- M4: Packaging & deploy
- M5: Observability & docs

## Work Breakdown (Tasks)
- Task ID, summary, owner, estimate, dependencies, target milestone
- For each task: **Acceptance Tests** (bullet list), **Files/Interfaces** touched

## Risks & Mitigations
- Risk → Impact → Likelihood → Mitigation → Trigger

## Test Strategy
- Unit/Property/Mutation
- Integration/Contract
- E2E/Smoke/Perf (thresholds)

## Security & Compliance
- Secret handling, authZ/authN, threat model notes, scans to run

## Observability
- Metrics, logs, traces to emit; dashboards to add/modify

## Rollout Plan
- Env order, migration steps, feature flags, rollback triggers

## Validation Gates
- Gate A (Design sign-off)
- Gate B (Test plan sign-off)
- Gate C (Pre-merge quality bar)
- Gate D (Pre-deploy checks)

## Success Metrics
- KPIs / SLOs, error budgets, perf ceilings

## References
- Research doc sections, GitHub permalinks, tickets

## Agents

- you can deploy maxium TWO subagents 
- context-synthesis subagent
- codebase-analyzer subagent

## Final Gate
- Output a short summary with: plan path, milestones count, gates, and next command hint: `/execute "<plan_path>"`

- this mustbe be a singualr focused plan, we cna have ONE other option in the same document but in general we MUST have a singular focused plan on execution. 


  DO NOT CODE YOU WILL BE PUNISHED FOR CODING 

  SAVE THE DOCUMENT YOU MUST SAVE IN THE CORRECT FORMAT FOR THE NEXT DEV

  ALWAYS FOLLOW BEST PRACTISES