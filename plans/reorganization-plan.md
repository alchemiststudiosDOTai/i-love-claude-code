# Project Reorganization Plan

## Overview
This plan reorganizes the Claude Code special directories in `i-love-claude-code`:
- `commands/` - Slash commands
- `agents/` - Specialized AI agents
- `skills/` - Claude Skills
- `hooks/` - Hook scripts and configuration

## Current State Analysis

### Issues Identified:
1. **Typo**: `tech-docs-maitainer.md` → should be `tech-docs-maintainer.md`
2. **Flat structure**: Commands and agents are mostly in root directories without categorization
3. **Outdated references**: `commands/README.md` references non-existent paths
4. **Inconsistent naming**: Mixed patterns in file names
5. **Scattered skills**: Only one skill (`ontological-documentation/`) exists but has nested structure
6. **Hooks not categorized**: Scripts and Python validators are mixed together

## Proposed Directory Structure

```
i-love-claude-code/
├── commands/                          # Slash commands (organized by category)
│   ├── python/                        # Python-related commands
│   │   └── (moved python commands here)
│   ├── web/                           # Web development commands
│   │   └── (moved web commands here)
│   ├── devops/                        # DevOps commands
│   │   └── (moved devops commands here)
│   ├── context-engineering/           # Context engineering workflow (existing)
│   │   ├── research.md
│   │   ├── plan.md
│   │   └── execute.md
│   ├── quality-assurance/             # QA commands
│   │   └── (moved QA commands here)
│   ├── integration/                   # Integration commands (Linear, GitHub)
│   │   └── (moved integration commands here)
│   ├── utilities/                     # Utility commands
│   │   └── (moved utility commands here)
│   └── README.md                      # Overview of all commands
│
├── agents/                            # Specialized agents (organized by category)
│   ├── analysis/                      # Code analysis agents
│   │   └── (moved analysis agents here)
│   ├── development/                   # Development agents
│   │   └── (moved development agents here)
│   ├── documentation/                 # Documentation agents
│   │   └── (moved documentation agents here)
│   ├── research/                      # Research agents
│   │   └── (moved research agents here)
│   ├── security/                      # Security agents
│   │   └── (moved security agents here)
│   ├── performance/                   # Performance agents
│   │   └── (moved performance agents here)
│   └── README.md                      # Overview of all agents
│
├── skills/                            # Claude Skills
│   ├── ontological-documentation/     # Existing skill
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   │   ├── examples/
│   │   │   └── ontology-templates/
│   │   ├── references/
│   │   └── scripts/
│   ├── (future skills would go here as new folders)
│   └── README.md                      # How to create skills
│
├── hooks/                             # Claude Code Hooks
│   ├── security/                      # Security validation hooks
│   │   └── security-validator.py
│   ├── formatting/                    # Code formatting hooks
│   │   └── auto-formatter.sh
│   ├── notification/                  # Notification hooks
│   └── README.md                      # Hook documentation
│
└── docs/                              # Centralized documentation
    ├── PROJECT_STRUCTURE.md
    ├── CONTRIBUTION_GUIDE.md
    └── VALIDATION_GUIDE.md
```

## Task List

### Phase 1: Fix Critical Issues
- [ ] Fix typo: rename `agents/tech-docs-maitainer.md` to `agents/tech-docs-maintainer.md`
- [ ] Fix typo in `agents/README.md` reference to maintainer agent

### Phase 2: Create Category Directories
- [ ] Create `commands/python/`
- [ ] Create `commands/web/`
- [ ] Create `commands/devops/`
- [ ] Create `commands/quality-assurance/`
- [ ] Create `commands/integration/`
- [ ] Create `commands/utilities/`
- [ ] Create `agents/analysis/`
- [ ] Create `agents/development/`
- [ ] Create `agents/documentation/`
- [ ] Create `agents/research/`
- [ ] Create `agents/security/`
- [ ] Create `agents/performance/`
- [ ] Create `docs/`

### Phase 3: Move Commands to Categories
- [ ] Move `commands/coderabbitai.md` → `commands/integration/`
- [ ] Move `commands/context-compact.md` → `commands/utilities/`
- [ ] Move `commands/deep-research.md` → `commands/context-engineering/` (or merge)
- [ ] Move `commands/execute-from-deep-research.md` → `commands/context-engineering/`
- [ ] Move `commands/fagan-inspection.md` → `commands/quality-assurance/`
- [ ] Move `commands/implementation-from-deep-research.md` → `commands/context-engineering/`
- [ ] Move `commands/linear-continue-debugging.md` → `commands/integration/`
- [ ] Move `commands/linear-continue-work.md` → `commands/integration/`
- [ ] Move `commands/phase-planner.md` → `commands/utilities/` (or context-engineering/)
- [ ] Move `commands/smart-git.md` → `commands/utilities/`
- [ ] Move `commands/three-step-workflow.md` → `commands/context-engineering/`
- [ ] Keep `commands/context-engineering/` contents as-is (already organized)

### Phase 4: Move Agents to Categories
- [ ] Move `agents/bug-issue-creator.md` → `agents/development/`
- [ ] Move `agents/code-clarity-refactorer.md` → `agents/development/`
- [ ] Move `agents/code-synthesis-analyzer.md` → `agents/analysis/`
- [ ] Move `agents/codebase-analyzer.md` → `agents/analysis/`
- [ ] Move `agents/codebase-locator.md` → `agents/analysis/`
- [ ] Move `agents/git-diff-documentation-agent.md` → `agents/documentation/`
- [ ] Move `agents/memory-profiler.md` → `agents/performance/`
- [ ] Move `agents/multi-agent-synthesis-orchestrator.md` → `agents/research/`
- [ ] Move `agents/prompt-engineer.md` → `agents/documentation/`
- [ ] Move `agents/security-orchestrator.md` → `agents/security/`
- [ ] Move `agents/tdd-python.md` → `agents/development/`
- [ ] Move `agents/tech-docs-maintainer.md` → `agents/documentation/`
- [ ] Move `agents/technical-docs-orchestrator.md` → `agents/documentation/`
- [ ] Move `agents/web-docs-researcher.md` → `agents/research/`
- [ ] Move `agents/guide.md` → `agents/` (keep in root, update name to SUBAGENTS_GUIDE.md)

### Phase 5: Consolidate Documentation
- [ ] Create `docs/PROJECT_STRUCTURE.md` - Overview of the reorganized structure
- [ ] Create `docs/CONTRIBUTION_GUIDE.md` - How to add new commands/agents
- [ ] Simplify `commands/README.md` to point to category READMEs
- [ ] Simplify `agents/README.md` to point to category READMEs
- [ ] Update `README.md` to reflect new structure
- [ ] Update `CLAUDE.md` to reflect new structure

### Phase 6: Update Internal References
- [ ] Update `commands/README.md` references to new command paths
- [ ] Update `commands/COMMANDS.md` examples to use new paths
- [ ] Update all README files to reflect new structure
- [ ] Update any @file references that point to moved files

### Phase 7: Cleanup
- [ ] Remove empty directories after moves
- [ ] Verify all commands still work with validator
- [ ] Update any scripts that reference old paths
- [ ] Create/update `.claude/` symlinks if needed

## Validation Steps

After reorganization:
1. Run `python validate_commands.py commands/` to verify all commands are valid
2. Test that slash commands are discoverable
3. Verify agent references work
4. Check that all README links point to correct locations

## Rollback Plan

If issues arise:
1. Keep original files until validation passes
2. Use git to track all moves
3. Can revert with `git checkout HEAD -- .` if needed
