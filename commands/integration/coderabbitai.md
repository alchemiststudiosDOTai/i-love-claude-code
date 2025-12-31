---
allowed-tools: View, Edit, Bash(gh:*), Bash(grep:*), Bash(find:*), Bash(git:*)
argument-hint: [issue-number]
description: Normalize a GitHub issue by asking @coderabbitai to outline and structure it
---


# CodeRabbitAI Issue Analysis

Tag @coderabbitai on GitHub issue for: $ARGUMENTS

## Context Gathering
<!-- Analyze existing project state before making changes -->
- Target issue: !`gh issue view $ARGUMENTS --json title,body,labels`
- Issue content: !`gh issue view $ARGUMENTS`
- Repository context: @.git/config
- Related files: !`grep -ri "$(gh issue view $ARGUMENTS --json title --jq .title)" .claude/ || true`
- Project structure: !`find . -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.ts" | head -20`
- Current branch: !`git branch --show-current`

## Planning Phase
<!-- Document approach before implementation -->
Create PLANNING_DOCUMENT.md with:
1. Issue analysis and categorization
2. @coderabbitai tagging strategy
3. Expected research outcomes
4. Integration with existing workflow
5. Success metrics for structured analysis

## Implementation Steps

### Step 1: Issue Analysis
<!-- First implementation phase -->
- Review issue title and description
- Identify key technical components
- Check for existing related discussions
- Validation check: !`gh issue view $ARGUMENTS --json assignees,labels`
- Expected outcome: Clear understanding of issue scope

### Step 2: Tag @coderabbitai
<!-- Main implementation work -->
```markdown
@coderabbitai Please provide a structured research-style analysis:

# Research – Issue $ARGUMENTS
**Date:** {{date}}
**Owner:** @coderabbitai
**Phase:** Research

## Goal
Summarize all *existing knowledge* before any new work.

## Findings
- Relevant files & why they matter:
   - `<file>` → `<reason>`
   - `<file>` → `<reason>`

## Key Patterns / Solutions Found
- `<pattern>`: short description, relevance

## Knowledge Gaps
- Missing context or details for next phase

## References
- Links or filenames for full review
```
- Add comment to GitHub issue
- Monitor for @coderabbitai response
- Progress check: !`gh issue view $ARGUMENTS --json comments`

### Step 3: Integration
<!-- Connect with existing system -->
- Link analysis to existing documentation
- Update issue labels if needed
- Compatibility check: !`gh issue list --label enhancement`
- Update related files: @.claude/

### Step 4: Testing
<!-- Comprehensive testing phase -->
- Verify @coderabbitai response: !`gh issue view $ARGUMENTS`
- Check analysis completeness
- Edge cases:
  - Complex technical issues
  - Multi-component problems
- Response quality check: Manual review of structured output

### Step 5: Documentation
<!-- Update project documentation -->
- Update issue tracking documentation
- Add analysis to project knowledge base
- Document @coderabbitai integration workflow
- Record successful patterns for future use

## Validation & Finalization
<!-- Final checks before completion -->
- Verify @coderabbitai tagged successfully: !`gh issue view $ARGUMENTS`
- Check structured response received
- Validate analysis quality and completeness
- Manual verification checklist:
  - [ ] @coderabbitai responded with structured analysis
  - [ ] All key components identified
  - [ ] Knowledge gaps clearly outlined
  - [ ] References provided for further investigation

## Success Criteria
<!-- Measurable outcomes that indicate completion -->
- ✓ Issue successfully tagged with @coderabbitai
- ✓ Structured research report appears in issue thread
- ✓ Analysis includes relevant files and patterns
- ✓ Knowledge gaps clearly identified
- ✓ No additional files created unnecessarily
- ✓ Integration with existing workflow maintained

## Rollback Plan
<!-- In case something goes wrong -->
- Backup location: GitHub issue history
- Rollback command: !`gh issue edit $ARGUMENTS --remove-label coderabbitai`
- Verification after rollback: !`gh issue view $ARGUMENTS --json labels`

## Notes
<!-- Additional context or warnings -->
- @coderabbitai responses may take time to appear
- Ensure GitHub CLI is authenticated and configured
- Complex issues may require multiple interaction rounds
- Future enhancement: Automated follow-up on incomplete responses

