---
allowed-tools: Edit, View, Bash(git:*), Bash(python:*), Bash(pytest:*), Bash(mypy:*), Bash(black:*), Bash(coverage:*), Bash(mutmut:*), Bash(docker:*), Bash(trivy:*), Bash(hadolint:*), Bash(dive:*), Bash(npm:*), Bash(kubectl:*), Bash(helm:*), Bash(lighthouse:*), Bash(jq:*), Bash(curl:*), Bash(gh:*)
description: Executes a plan with gated checks, atomic commits, build/package/deploy, full validation, and immutable execution logs
writes-to: memory-bank/execute/
---

# Execute Plan

Execute the implementation according to: $ARGUMENTS  (path to a Plan doc)

## Initial Setup (prompt)
"I'm ready to execute. Please provide the path to the Plan document in memory-bank/plan/."



## Strict Ordering
1) Read plan FULLY → 2) Pre-flight checks → 3) Implement by tasks → 4) Validate gates → 5) Package/Deploy → 6) Post-deploy verification → 7) Persist log

## Step 1 — Read Plan & Lock Context
- Read FULL `memory-bank/plan/<file>.md`.
- Extract: milestones, tasks (IDs), acceptance tests, gates, rollout, success metrics.

## Step 2 — Pre-Flight Snapshot
Record into execution log header:
- Active branch: !`git branch --show-current`
- ROLL BACK POINT: YOU MUST CREATE A GIT COMIMT WITH A ROLLBACK POINT. 

Create `memory-bank/execute/YYYY-MM-DD_HH-MM-SS_<topic>.md`:

You MUST keep this SINGULAR documen in synch as you work

DO NOT MAKE MULTIPLE DOCUMENT WILL BE YOUR LOG FOR THE EXCUTION

---
title: "<topic> – Execution Log"
phase: Execute
date: "{{timestamp}}"
owner: "{{agent_or_user}}"
plan_path: "memory-bank/plan/<file>.md"
start_commit: "<short_sha>"
env: {target: "local|staging|prod", notes: ""}
---

## Pre-Flight Checks
- DoR satisfied?
- Access/secrets present?
- Fixtures/data ready?
- If any **NO** → abort and append **Blockers** section.

## Step 3 — Task-By-Task Implementation (Atomic)
For each Task (in plan order):
1. Create/confirm rollback
2. Implement minimal slice aligned with acceptance tests
3. Run local quality bar
4. Commit atomic change with Task ID in message
5. Update **Execution Log** with:
   - Files touched, commands, outputs (trimmed), coverage deltas, notes

## Step 4 — Quality Gates (Enforced)
- Gate C (Pre-merge):
  - Tests pass
  - Coverage ≥ plan threshold (e.g., 90%+ new/changed lines)
  - Type checks clean
  - Linters OK
  
- If any gate FAILS → record failure + remediation then dont roll back just stop and ask the user for next steps



## Step 5 — Permalinks & Artifacts
- If commits pushed:
  - !`gh repo view --json owner,name`
  - Attach permalinks to PRs/commits and to artifacts (build logs, coverage HTML)
- Persist artifact pointers in **Execution Log**.

## Execution Log Template (append as you go)
### Task <ID> – <Summary>
- Commit: `<short_sha>`
- Commands:
  - `<cmd>` → `<trimmed output>`
- Tests/coverage:
  - `<result>`
- Notes/decisions:
  - `<why>`

### Gate Results
- Gate C: pass/fail + evidence
- Security: pass/fail + evidence
- Perf/PWA (if applicable): metrics

### Deployment Notes
- Staging → Prod timestamps
- Smoke/E2E results
- SLO/SLA snapshot

### Post-Deploy Verification
- Error rates, latencies, dashboards screenshots/links
- On-call runbook links

### Follow-ups
- TODOs, tech debt, docs to update

## Success Criteria (auto-check)
- All planned gates passed
- Rollout completed or rollback clean
- KPIs/SLOs within thresholds
- Execution log saved to `memory-bank/execute/` and linked back to Plan

# Execution Report – <topic>

**Date:** {{date}}  
**Plan Source:** <plan file>  
**Execution Log:** <log file>

## Overview
- Environment: local|staging|prod
- Start commit: <sha>
- End commit: <sha>
- Duration: Xh Ym
- Branch: <branch>
- Release: <tag|helm release>

## Outcomes
- Tasks attempted: N
- Tasks completed: N
- Rollbacks: Y/N
- Final status: ✅ Success | ❌ Failure

## Gate Results
- Tests: pass/fail summary
- Coverage: X% (target Y%)
- Type checks: pass/fail
- Security scans: # issues
- Perf/PWA scores: numbers

## Issues & Resolutions
- <task ID> – <issue> → <fix>
- <task ID> – <issue> → <rollback>

## Deployment Notes
- Staging deploy: success/fail
- Prod deploy: success/fail
- Smoke/E2E results
- Observability checks

## Success Criteria
- Which criteria met vs missed

## Next Steps
- Follow-ups, tech debt, docs to update

## References
- Plan doc
- Execution log
- GitHub permalinks


CLEARLY SUMMARIZE WHA YOU DID AND TOUCHED

YOU ARE CODING AS YOU UPDATE THIS DOCUMENT 

SAVE THE DOCUMENT YOU MUST SAVE IN THE CORRECT FORMAT FOR THE NEXT DEV

ALWAYS FOLLOW BEST PRACTISES

THIS IS THE MOST IMPORTANT PART OF THIS PROMPT:MAKE THE DOCUMENT AND UPDATE AS YOU WORK.

AFTER THE WORK IS DONE 

DEPLOY 3 SUBAGENTS at most

- codebase-analyzer to outline your code changes in relation to the codebase 

- antipattern-sniffer any new code MUST be evaluted by this subagent 

- context-synthesis a agent to gather context as needed 

