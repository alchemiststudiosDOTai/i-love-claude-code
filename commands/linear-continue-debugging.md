---
allowed-tools: View, Edit, Bash, Git, Linear, DeepWiki, SequentialThinking
description: Continue debugging a Linear issue with systematic analysis
---

# Linear Continue Debugging

Continue debugging Linear issue: $ARGUMENTS

<ultrathink>
Resume systematic debugging. Use scientific method. Leverage all available tools. Find root cause, not symptoms.
</ultrathink>

<megaexpertise type="advanced-debugging-specialist">
The assistant should combine systematic thinking, deep analysis, and comprehensive tooling to extract maximum understanding from the bug.
</megaexpertise>

<context>
Continuing debugging for: $ARGUMENTS
Need to understand bug state, leverage advanced tools, and find root cause
</context>

<requirements>
- Find Linear issue and understand bug context
- Use systematic thinking for hypothesis generation
- Leverage deepwiki for library/framework understanding
- Apply scientific debugging methodology
- Document findings thoroughly
</requirements>

<actions>
1. Find Linear issue and bug context:
   - Extract issue ID from branch: git rev-parse --abbrev-ref HEAD
   - Get full issue details: mcp_linear.get_issue(id)
   - Review comments for reproduction steps and symptoms
   - Check linked PRs for previous fix attempts
   
2. Use mcp__sequential-thinking__sequentialthinking for systematic analysis:
   - Start with thought: "What are all possible causes of this bug?"
   - Generate multiple hypotheses ranked by likelihood
   - Consider edge cases and race conditions
   - Think through implementation details step-by-step
   - Question assumptions and revise thinking as needed
   - Use branch_from_thought for exploring alternative theories
   
3. Leverage mcp__deepwiki for deep understanding:
   - If bug involves external library: mcp__deepwiki__ask_question(repoName="org/repo", question="How does X handle Y?")
   - Get implementation details: mcp__deepwiki__read_wiki_contents(repoName="org/repo")
   - Understand design decisions that might affect the bug
   - Check for known issues or gotchas in the library
   
4. Apply scientific debugging:
   - Design specific tests for each hypothesis
   - Add strategic logging with context:
     ```python
     logger.debug(f"[BUG-{issue_id}] State before: {state}, Inputs: {inputs}, Stack: {inspect.stack()[1].function}")
     ```
   - Use binary search to isolate problem area
   - Create minimal reproduction case
   - Test in different environments/configurations
   
5. Advanced debugging techniques:
   - Use debugger with conditional breakpoints
   - Memory profiling if suspecting leaks
   - Performance profiling for timing issues
   - Network inspection for API/communication bugs
   - Database query analysis for data issues
   
6. Root cause analysis:
   - Use mcp__sequential-thinking to validate findings
   - Distinguish between symptoms and root cause
   - Understand why the bug wasn't caught earlier
   - Identify related code that might have same issue
   
7. Document and fix:
   - Write failing test that reproduces the bug
   - Implement minimal fix addressing root cause
   - Add defensive coding to prevent recurrence
   - Commit with Linear magic words:
     - "Refs TEAM-123" for investigation commits
     - "Fixes TEAM-123" for final bug fix
   - Update Linear with detailed findings:

     ```javascript
     mcp__linear__create_comment(issueId, body="""
     ## Root Cause Analysis
     - Hypothesis tested: ...
     - Root cause: ...
     - Why it happened: ...
     - Fix approach: ...
     """)
     ```

7. Knowledge capture:
   - Create `.claude/debugging/[bug-pattern].md` with learnings
   - Update documentation if user-facing issue
   - Add code comments explaining non-obvious fixes
   - Consider if architectural change needed to prevent class of bugs
</actions>

Debugging is detective work. The assistant should use all tools available - systematic thinking for hypotheses, deepwiki for understanding, and scientific method for proof.

Take a deep breath in, count 1... 2... 3... and breathe out. The assistant is now centered and should not hold back but give it their all.