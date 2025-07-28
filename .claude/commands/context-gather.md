---
description: Multi-agent context gatherer using Task tool for MANDATORY parallel execution
allowed-tools: Task(*), Bash(*), Read(*), Edit(*), WebSearch(*)
---

# /context/gather — True Multi-Agent Context Collector

Gather comprehensive context about an issue/bug/feature using STRICTLY PARALLEL subagents.

**CRITICAL RULE**: You MUST NOT code. You are STRICTLY an agent manager who deploys agents IN PARALLEL to gather context. Sequential agent execution is FORBIDDEN. 

**Usage**: `/context/gather "description of issue"`

## Implementation

### Phase 1: Planning Agent

First, analyze the request and create a search plan:

```
If the request is unclear, ask for:
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

**CRITICAL**: After receiving the plan, you MUST launch EXACTLY 2 specialized search agents IN PARALLEL. Sequential execution is FORBIDDEN - both agents MUST be launched simultaneously in a single message with multiple Task tool invocations.

```
Task 1: "Code & System Agent"
Prompt: "Using this search plan: [PLAN_OUTPUT]
COMPREHENSIVELY investigate ALL code and system aspects:
- Execute code searches using rg -n -S for symbol searching
- Use git grep for version-controlled content
- Use fd for file discovery
- Find ALL implementations, usages, and dependencies
- Examine ALL test files related to the issue
- Investigate ALL configuration files
- Check ALL environment variables
- Review CI/CD configurations
- Analyze database migrations if applicable
- Include current test status and coverage
Return findings with file paths and line numbers."

Task 2: "Documentation & Analysis Agent"  
Prompt: "Using this search plan: [PLAN_OUTPUT]
THOROUGHLY search and analyze ALL documentation:
- README files at all levels
- API documentation and specifications
- OpenAPI/Swagger specs
- Architecture and design docs
- Code comments and docstrings
- Wiki pages if available
- Change logs and release notes
- Any technical documentation
Use Read() for large files, WebSearch for external docs.
Analyze patterns and provide insights on system behavior."
```

**ENFORCEMENT**: These agents MUST be launched together in ONE message. NEVER launch them sequentially. The power of this command comes from TRUE PARALLEL EXECUTION. Only use web search if you absolutely need to. If it doesn't relate to the issue, do not use web search.

### Phase 3: QA & Validation

**IMMEDIATELY** after both agents complete, launch a QA agent to validate findings:

```
Task: "QA Validation Agent"
Prompt: "Review the combined findings from BOTH parallel agents:
[CODE_SYSTEM_FINDINGS]
[DOCUMENTATION_ANALYSIS_FINDINGS]

Validate comprehensiveness by checking for:
- Inconsistencies or contradictions between findings
- Missing critical information
- Stale or incorrect file paths
- Gaps in understanding
- Unexamined areas that need investigation

Output a validation report with:
1. Confidence score (0-100)
2. Specific gaps found
3. Recommended additional searches if needed
4. Areas requiring clarification"
```

If confidence < 80, iterate up to 3 times:
- Launch targeted search agents IN PARALLEL for specific gaps
- Update findings
- Re-run QA validation

### Phase 4: Synthesis Agent

Once QA validation passes or after 3 iterations:

```
Task: "Context Synthesis Agent"
Prompt: "You have validated context findings from 2 parallel search agents: 
[CODE_SYSTEM_FINDINGS]
[DOCUMENTATION_ANALYSIS_FINDINGS]
[QA_VALIDATION_REPORT]

Create a COMPREHENSIVE context dossier with:
1. Executive Summary
2. System Architecture (relevant parts)
3. Key Files & Their Roles
4. Call Flow / Data Flow
5. Relevant APIs & Endpoints
6. Configuration Details
7. Test Coverage Analysis
8. Documentation Insights
9. Open Questions & Next Steps

Format as markdown with clear sections.
Save to: .claude/context/context-{slug}-{date}.md"
```

### Phase 5: Final Output

After QA passes or 3 iterations:
1. Save final dossier to `.claude/context/`
2. If still uncertain, present specific questions to user
3. Provide summary of findings and dossier location

## Example Execution Flow

```
User: /context/gather "description of issue to investigate"

Claude: Analyzing the issue using the context-gather command approach.

Claude: Launching Context Planning Agent...
[Task launches, returns search plan]

Claude: Now launching the two parallel search agents to investigate comprehensively:
[Tasks launch SIMULTANEOUSLY in ONE message]

Claude: Both agents complete. Running QA validation to verify findings:
[Task validates findings, may trigger parallel iterations]

Claude: QA complete. Launching synthesis agent to create comprehensive dossier:
[Task creates comprehensive dossier]

Claude: Context gathering complete!
📄 Saved to: .claude/context/context-[issue-slug]-[date].md

Key findings:
- Root cause identified with specific location
- Affected components and their relationships  
- Test coverage gaps discovered
- Recommended implementation approach
```

