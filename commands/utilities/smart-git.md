---
allowed-tools: View, Bash(git:*), Bash(sed:*), Bash(awk:*)
description: Stage all changes and generate smart commit with inline diff
---

# Smart Git Commit & Push

## Objectives

- Create a single commit that embeds the change in formatted way to the commit message.
- Push to the same branch we are on now.
- Exit cleanly with clear status.

## Guardrails

- Never run destructive operations (no hard resets, no forced pushes).
- If no working-tree changes exist, report “no local changes” and stop.
- Default `MAX_LINES` for the inline diff is 200 lines.

## Workflow

### 1) Context Gathering

- Determine repository root; if not a Git repo, stop with a helpful message.
- Determine the current branch and store as `BRANCH`.
- Check whether an upstream tracking ref exists; note as `HAS_UPSTREAM` (yes/no).
- Capture ahead/behind status relative to upstream if present.

### 2) Pre-commit Diff Snapshot (vs origin/BRANCH)

- Compute a file-level diff summary and store as `DIFF_STAT`.
- Compute a unified diff (context 3) and truncate to `MAX_LINES`; store as `DIFF_DETAIL`.

### 3) Stage Changes

- If there are no local changes, report and stop.
- Stage all modifications, additions, and deletions.

### 4) Construct Commit Message

- always commit liek "feature:" "test:" "chore:" etc use common sense.
- Title: “Smart commit on {BRANCH}”.
- Body sections:

  - “Changes Summary:” followed by `DIFF_STAT`.
  - “Detailed Diffs (first {MAX_LINES} lines):” followed by `DIFF_DETAIL`.
  - Footer: “All local changes staged and pushed by smart-commit”.

### 5) Commit

- Assume the user wants to git add .
- Create the commit using the constructed message.

### 6) Push

- when the commit hooks pass, then push
- if the pre-commit hooks fail, take a deep breath, if it is NOT on MASTER you can run -n to skip them
- if the branch is MASTER you MUST NOT push alert the user
- alwasy confirm the pre-commit hooks status before pushing

## Validation

- Confirm the last commit message includes both “Changes Summary:” and “Detailed Diffs”.
- Confirm working tree is clean after push.
- Report final ahead/behind status; success means local and remote are synchronized.

## Success Criteria

- Commit message contains file-level stats and a truncated inline diff.
- All local changes are staged and committed.

