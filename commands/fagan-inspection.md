---
allowed-tools: Edit, View
description: Fagan-style inspection for analysis only; identifies defects and prepares findings for the next devoir agent
---

# Fagan Inspection (Analysis-Only)

Run a formal analysis inspection for: $ARGUMENTS

**Purpose**: Conduct comprehensive defect analysis WITHOUT fixing. Results are prepared for the next devoir agent in the workflow.

## Context Gathering
- Artifact(s) under review: @path/to/artifacts/
- Related refs (reqs/specs/logs/tickets): @docs/ @issues/
- Define roles: Moderator, Author, Reader, Inspectors

## Planning
Create FAGAN_PLAN.md:
1. Scope & objective (single issue/defect cluster)
2. Entry criteria & exit criteria
3. Defect taxonomy & logging location
4. Timebox & metrics (defects/hour, rework time)

## Agent Orchestration (Parallel Subagents)
- Assess candidate subagents and pick the two best-fit for this issue type (e.g., code-synthesis-analyzer, codebase-locator)
- Run both subagents in parallel on the same artifacts.
- Merge outputs, deduplicate, and rank by severity/likelihood.
- Provide a brief rationale for subagent choice and any coverage gaps.
- **Analysis Focus**: Subagents perform detection and documentation only, no remediation.

## Execution (Fagan Analysis Steps)
### 1) Overview
- Moderator briefs; Author clarifies intent; confirm artifact versions.

### 2) Preparation
- Inspectors review individually; note suspected defects with locations.

### 3) Inspection Meeting
- Reader walks artifact; raise defects (no solution debates).
- Moderator logs: ID, location, type, severity, evidence.
- **ANALYSIS ONLY**: Document findings without implementing fixes.

### 4) Results Preparation
- Compile comprehensive defect report with detailed findings.
- Rank defects by severity/impact for next agent prioritization.
- Package analysis results for handoff to devoir agent.

## Documentation
- Store logs, merged subagent report, and metrics in @docs/reviews/
- Summary note: scope, top defects, analysis completeness, lessons learned.
- **Analysis Report**: Structured findings document for next devoir agent consumption.

## Validation & Exit
- Checklist:
  - [ ] All critical defects identified and documented
  - [ ] Analysis coverage complete across all targeted areas
  - [ ] Subagent findings merged and archived
  - [ ] Metrics captured; analysis quality validated
  - [ ] Results properly formatted for next devoir agent

## Success Criteria
- ✓ Comprehensive defect analysis completed with full documentation
- ✓ Parallel subagent analysis completed with rationale
- ✓ Analysis results structured and ready for handoff to next agent

## Next Agent Handoff
- **Analysis Package**: Complete defect findings with severity rankings
- **Context Bundle**: All relevant artifacts, logs, and subagent reports  
- **Recommendations**: Suggested next steps and agent types for remediation
- **Metadata**: Analysis scope, coverage areas, and confidence levels

## Rollback (Analysis Context Only)
- Record analysis state and checkpoint locations
- Preserve original artifact versions for reference
- Maintain defect ID traceability for future agents

## Notes
- Tech-agnostic; use with code, designs, specs, runbooks
- Tune subagent pairing to issue type
- **ANALYSIS ONLY**: This process does NOT implement fixes
- Results feed into downstream devoir agents for implementation 
