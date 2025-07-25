---
description: Multi-agent context gatherer using Task tool for true parallel execution
allowed-tools: Task(*), Bash(*), Read(*), Edit(*), WebSearch(*)
---

# /context/gather — True Multi-Agent Context Collector

Gather comprehensive context about an issue/bug/feature using parallel subagents.

**Usage**: `/context/gather "description of issue"`

## Implementation

### Phase 1: Planning Agent

First, I'll analyze your request and create a search plan:

```
If the request is unclear, I'll ask for:
- Which service/module/file area?
- Exact error messages or symptoms?
- Environment (dev/staging/prod)?
- Any relevant endpoints or functions?
```

Then launch the planning agent:

```
Task: "Context Planning Agent"
Prompt: "Create a detailed search plan for investigating: [$ARGUMENTS]. 
Output a structured plan including:
1. Code patterns to search (symbols, error codes, endpoints)
2. Key directories and files to examine
3. Config files and environment variables to check
4. Tests that might be relevant
5. Documentation to review
Format as JSON for easy parsing by other agents."
```

### Phase 2: Parallel Search Agents

After receiving the plan, launch multiple specialized search agents in parallel:

```
Task 1: "Code Search Agent"
Prompt: "Using this search plan: [PLAN_OUTPUT]
Execute code searches using:
- rg -n -S 'patterns' for symbol searching
- git grep for version-controlled content
- fd for file discovery
Focus on finding implementations, usages, and dependencies.
Return findings with file paths and line numbers."

Task 2: "Documentation Agent"  
Prompt: "Using this search plan: [PLAN_OUTPUT]
Search for and analyze:
- README files
- API documentation
- OpenAPI/Swagger specs
- Architecture docs
- Comments in code
Use Read() for large files, WebSearch for external docs."

Task 3: "Test & Config Agent"
Prompt: "Using this search plan: [PLAN_OUTPUT]
Investigate:
- Test files related to the issue
- Configuration files
- Environment variables
- CI/CD configurations
- Database migrations
Include current test status if available."

Task 4: "Logs & Runtime Agent"
Prompt: "Using this search plan: [PLAN_OUTPUT]
If applicable, examine:
- Error logs
- Stack traces
- Performance metrics
- Runtime configurations
- Deployment histories"
```

### Phase 3: Synthesis Agent

Once all search agents complete:

```
Task: "Context Synthesis Agent"
Prompt: "You have context findings from 4 search agents: 
[CODE_FINDINGS]
[DOC_FINDINGS]
[TEST_CONFIG_FINDINGS]
[LOGS_RUNTIME_FINDINGS]

Create a comprehensive context dossier with:
1. Executive Summary
2. System Architecture (relevant parts)
3. Key Files & Their Roles
4. Call Flow / Data Flow
5. Relevant APIs & Endpoints
6. Configuration Details
7. Test Coverage Analysis
8. Open Questions

Save to: .claude/context/context-{slug}-{date}.md"
```

### Phase 4: QA & Iteration Loop

Launch a QA agent to validate findings:

```
Task: "QA Validation Agent"
Prompt: "Review this context dossier: [DOSSIER]
Check for:
- Inconsistencies or contradictions
- Missing critical information
- Stale or incorrect paths
- Gaps in understanding

Output a validation report with:
1. Confidence score (0-100)
2. Specific gaps found
3. Recommended additional searches"
```

If confidence < 80, iterate up to 3 times:
- Launch targeted search agents for specific gaps
- Update the dossier
- Re-run QA validation

### Phase 5: Final Output

After QA passes or 3 iterations:
1. Save final dossier to `.claude/context/`
2. If still uncertain, present specific questions to user
3. Provide summary of findings and dossier location

## Key Differences from Non-Working Version

1. **Uses Task tool explicitly** - Each "agent" is a real subagent launched via Task
2. **Parallel execution** - Search agents run simultaneously, not sequentially  
3. **Clear handoffs** - Each agent receives specific inputs and produces specific outputs
4. **True independence** - Each subagent has its own context and search space
5. **Structured communication** - Agents pass data via clear formats (JSON, markdown)

## Example Execution Flow

```
User: /context/gather "API endpoint returning 500 errors on user profile updates"

Claude: Launching Context Planning Agent...
[Task launches, returns search plan]

Claude: Launching 4 parallel search agents...
[Tasks launch simultaneously]

Claude: All agents complete. Launching synthesis agent...
[Task creates dossier]

Claude: Running QA validation...
[Task validates, may trigger iteration]

Claude: Context gathering complete!
📄 Saved to: .claude/context/context-api-500-error-2025-01-24.md

Key findings:
- Root cause: Missing null check in UserProfileSerializer
- Affected endpoints: PUT /api/v2/users/{id}/profile
- Related test gaps: No test for null bio field
- Quick fix available in utils/validators.py
```

This approach creates true multi-agent behavior with independent, parallel execution - just like the working Multi-Mind command!/
