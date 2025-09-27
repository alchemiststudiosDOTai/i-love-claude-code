---
allowed-tools: Edit, View, Bash(git:*), Bash(python:*), Bash(pytest:*), Bash(mypy:*), Bash(black:*), Bash(npm:*), Bash(jq:*)
description: Generates a concrete implementation plan from a research doc, with milestones, tasks, gates
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
- Capture current git state (if git repository exists):
  - !`git rev-parse --git-dir 2>/dev/null && git rev-parse --short HEAD || echo "Not in a git repository"`
  - !`git rev-parse --git-dir 2>/dev/null && git status --porcelain || echo "Not in a git repository"`
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
- At most ONE new test if more test are needed we WILL NOT do that now 
- you will be punished for mutiple test at most ONE 


## References
- Research doc sections, GitHub permalinks, tickets

## Agents

- you can deploy maxium 3 subagents at one time and should do so
- context-synthesis subagent
- codebase-analyzer subagent

## Final Gate
- Output a short summary with: plan path, milestones count, gates, and next command hint: `/execute "<plan_path>"`

- this must be be a singualr focused plan, we can have ONE other option in the same document but in general we MUST have a singular focused plan on execution. 

  DO NOT CODE YOU WILL BE PUNISHED FOR CODING 

  SAVE THE DOCUMENT YOU MUST SAVE IN THE CORRECT FORMAT FOR THE NEXT DEV

  ALWAYS FOLLOW BEST PRACTISE and take a deep breath this is for execution
