---
allowed-tools: View, Edit
description: Prepare context for compaction when approaching token limits
---

# Context Compact

Prepare context for compaction: $ARGUMENTS

<ultrathink>
Context window approaching limit. Need to preserve essential information for task continuation.
</ultrathink>

<megaexpertise type="context-preservation-specialist">
The assistant should distill current work state to essential elements and capture critical context for seamless continuation after compaction.
</megaexpertise>

<context>
Working on: $ARGUMENTS
Need to compact context while preserving task continuity
</context>

<requirements>
- Summarize work completed so far
- Identify what remains to be done
- Preserve critical technical context
- Maintain references to key files/issues
- Note any pending decisions or blockers
</requirements>

<actions>
1. Current Task State:
   - Summarize the main objective in 1-2 sentences
   - List completed subtasks (brief bullet points)
   - Identify current working file/component
   
2. Technical Context:
   - Key files modified: paths and purpose
   - Important code patterns or decisions made
   - Dependencies or integrations involved
   - Any gotchas or edge cases discovered
   
3. Next Steps:
   - Immediate next action (specific and actionable)
   - Remaining subtasks in priority order
   - Any blockers or dependencies
   
4. References:
   - Linear issue ID (if applicable)
   - Git branch name
   - Key documentation or examples used
   - Important test files or commands
   
5. Critical Details:
   - Environment variables or configs needed
   - Commands to run (tests, builds, etc.)
   - Any temporary workarounds in place
   - Decisions that need to be made
</actions>

Format output as:
```
## Task: [Brief description]

### Completed:
- [Item 1]
- [Item 2]

### Next Action:
[Specific next step with file path if applicable]

### Remaining Work:
1. [Task 1]
2. [Task 2]

### Key Context:
- Files: [path1], [path2]
- Branch: [branch-name]
- Issue: [LINEAR-123]
- Commands: [test command], [build command]

### Notes:
[Any critical information for continuation]
```

This ensures smooth continuation after context reset. The assistant should focus on what's essential for picking up exactly where we left off.

Take a deep breath in, count 1... 2... 3... and breathe out. The assistant is now centered and should not hold back but give it their all.