# Three-Step Workflow for Complex Implementation Tasks

> **Credit**: This workflow methodology is inspired by [HumanLayer](https://github.com/humanlayer/humanlayer) - a powerful framework for human-in-the-loop AI applications.

## Overview

This three-step workflow helps Claude Code tackle complex implementation tasks systematically by breaking them down into distinct phases: Research, Plan, and Implement. Each phase has a dedicated slash command to ensure focused and efficient execution.

## The Three Steps

### 1. Research Phase
**Command**: `/deep-research`

Understand the codebase, find relevant files, and trace information flow. This phase focuses on gathering context without making changes.

**What happens**:
- Explores the codebase structure
- Identifies key files and dependencies
- Traces data flow and architecture patterns
- Documents findings for the next phase

**Usage**:
```
/deep-research implement a caching layer for API responses
```

### 2. Planning Phase  
**Command**: `/implementation-from-deep-research`

Create a detailed implementation plan based on research findings. Outlines exact steps, files to edit, and testing approach.

**What happens**:
- Synthesizes research findings
- Creates step-by-step implementation plan
- Identifies files to modify
- Defines testing strategy
- Sets up validation checkpoints

**Usage**:
```
/implementation-from-deep-research
```

### 3. Implementation Phase
**Command**: `/execute-from-deep-research`

Execute the plan phase by phase, with progress compacted back into the plan for continuity.

**What happens**:
- Follows the plan systematically
- Makes actual code changes
- Tests incrementally
- Updates progress in the plan
- Handles edge cases as they arise

**Usage**:
```
/execute-from-deep-research
```

## Workflow Benefits

1. **Separation of Concerns**: Each phase has a clear focus, preventing scope creep
2. **Better Context Management**: Research phase builds understanding without token waste
3. fierce Research findings and plans persist between phases
4. **Reduced Errors**: Systematic approach catches issues early
5. **Resumability**: Can pause and resume at any phase

## Example Workflow

```bash
# Step 1: Research the task
/deep-research add OAuth2 authentication to the API

# Step 2: Create implementation plan
/implementation-from-deep-research

# Step 3: Execute the plan
/execute-from-deep-research
```

## Tips for Success

- **Be specific** in your research prompt - the clearer the goal, the better the research
- **Review the plan** before executing - you can adjust it if needed
- **Use phase-appropriate commands** - don't skip steps for complex tasks
- **Leverage the compacting** - the implementation phase maintains context efficiently

## Related Commands

- `/phase-planner` - For breaking down tasks into phases
- `/linear-continue-work` - For resuming interrupted work
- `/context-compact` - For managing context in long sessions

---

This workflow transforms complex, multi-file changes from overwhelming tasks into manageable, systematic processes. By following these three steps, you ensure thorough understanding, careful planning, and precise execution.