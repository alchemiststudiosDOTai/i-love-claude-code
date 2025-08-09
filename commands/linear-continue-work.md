---
allowed-tools: View, Edit, Bash, Git, Linear
description: Continue work on a Linear issue by understanding state and planning next steps
---

# Linear Continue Work

Continue work on the following: $ARGUMENTS

<ultrathink>
Understand current state. Review what's done. Plan next steps systematically. Maintain momentum.
</ultrathink>

<megaexpertise type="project-continuation-specialist">
The assistant should seamlessly resume work, understand context, progress, blockers, and generate clear next actions.
</megaexpertise>

<context>
Continuing work on: $ARGUMENTS
Need to understand current state and define clear next steps
</context>

<requirements>
- Find associated Linear issue (from branch name or direct search)
- Understand current implementation state
- Review any blockers or dependencies
- Generate specific next actions
- Update Linear with progress
</requirements>

<actions>
1. Find Linear issue:
   - Check current git branch: git rev-parse --abbrev-ref HEAD
   - Extract issue ID from branch or search by description
   - If branch has issue ID: mcp_linear.get_issue_git_branch_name(id) to verify
   - Otherwise: mcp_linear.list_my_issues() or mcp_linear.list_issues(query="$ARGUMENTS")
   
2. Review issue context:
   - mcp_linear.get_issue(id) → get full details, attachments, description
   - mcp_linear.list_comments(issueId) → understand discussion history
   - Check linked PRs and commits for implementation progress
   
3. Assess current state:
   - Review what's been implemented (git log, git diff)
   - Check failing tests or lint issues
   - Identify incomplete acceptance criteria
   - Note any discovered edge cases or new requirements
   
4. Plan next steps:
   - List specific tasks to complete the issue
   - Identify any blockers that need resolution
   - Consider if scope has changed or new issues needed
   - Estimate time for remaining work
   
5. Update Linear:
   - mcp_linear.create_comment(issueId, body="Progress update with next steps")
   - Update issue status if needed: mcp_linear.update_issue(id, stateId)
   - Link any new discoveries or blockers
   - Use magic words in commits:
     - "Refs TEAM-123" for progress commits
     - "Fixes TEAM-123" for final completion

6. Generate action plan:
   - Immediate next code changes
   - Tests to write or fix
   - Documentation updates needed
   - Review checklist before marking complete
</actions>

This helps maintain flow state and ensures nothing is missed. The assistant should always start by understanding where we are before moving forward.

Take a deep breath in, count 1... 2... 3... and breathe out. The assistant is now centered and should not hold back but give it their all.