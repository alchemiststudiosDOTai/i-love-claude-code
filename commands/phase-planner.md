# Phase Planner Shortcut

A systematic workflow command for implementing features in phases with automatic commits after each subphase using a git worktree.

## Command: `/phase-planner`

### Purpose
Implements features through structured phases, with automatic linting, typechecking, building, and committing after each subphase completion using a git worktree.

**CRITICAL REQUIREMENTS:**
- **MUST use git worktree** for implementation
- Worktree name = issue name (e.g., `issue-1`)
- Create worktree in same directory as issue file
- Commit after EACH subphase completion
- **NEVER merge to main branch**
- **NEVER push outside the worktree**
- Violation of these rules will result in PUNISHMENT

### Workflow Pattern
```
Phase 1
├── 1.1: [First subphase]
│   ├── Implement
│   ├── Lint & Typecheck (new code only)
│   ├── Build
│   └── Commit if successful
├── 1.2: [Second subphase]
│   ├── Implement
│   ├── Lint & Typecheck (new code only)
│   ├── Build
│   └── Commit if successful
└── 1.3: [Third subphase]
    ├── Implement
    ├── Lint & Typecheck (new code only)
    ├── Build
    └── Commit if successful
```

### Command Implementation

```yaml
/phase-planner [feature-description] [issue-name]

# Worktree Setup (MANDATORY)
1. Identify issue name (e.g., "issue-1")
2. Create git worktree:
   - !git worktree add ./[issue-name] -b [issue-name]
   - cd into worktree directory
3. All work MUST happen in this worktree

# Phase Planning
1. Analyze the feature request
2. Break down into phases (usually 3-5 phases)
3. Each phase has 3-5 subphases
4. Create todo list for Phase 1 only

# Phase 1 Execution Loop
For each subphase (1.1, 1.2, 1.3...):
  1. Mark subphase as in_progress
  2. Implement the subphase functionality
  3. Run lint on new/modified files only:
     - @package.json check for lint command
     - !npm run lint -- [specific-files]
  4. Run typecheck on new/modified files only:
     - @package.json check for typecheck command  
     - !npm run typecheck -- [specific-files]
  5. If lint/typecheck pass:
     - !npm run build (if exists)
     - If build passes:
       - !git add [modified-files]
       - !git commit -m "feat(phase-1.x): [description]"
  6. Mark subphase as completed
  7. Continue to next subphase

# Documentation Update
After all Phase 1 subphases complete:
  - Update relevant documentation
  - Commit documentation changes

# Important Rules
- **MUST use git worktree** (named after issue)
- Stay in worktree directory only
- **NO merge to main branch**
- **NO git push operations**
- Only work on Phase 1
- Stop after each subphase completion
- Only lint/typecheck NEW code
- Commit after each successful subphase
- **PUNISHMENT for violating worktree rules**
```

### Example Usage

```bash
/phase-planner "Add user authentication with JWT tokens" "issue-auth-jwt"

# Claude Code will:
# 1. Create worktree:
!git worktree add ./issue-auth-jwt -b issue-auth-jwt
!cd issue-auth-jwt

# 2. Implement Phase 1:
Phase 1: Core Authentication Setup
├── 1.1: Create auth middleware
│   ├── Implement middleware
│   ├── !npm run lint src/middleware/auth.js
│   ├── !npm run typecheck src/middleware/auth.js
│   ├── !npm run build
│   └── !git commit -m "feat(phase-1.1): add auth middleware"
├── 1.2: Add JWT token generation
│   ├── Implement token service
│   ├── !npm run lint src/services/token.js
│   ├── !npm run typecheck src/services/token.js
│   ├── !npm run build
│   └── !git commit -m "feat(phase-1.2): add JWT token generation"
└── 1.3: Create login endpoint
    ├── Implement endpoint
    ├── !npm run lint src/routes/auth.js
    ├── !npm run typecheck src/routes/auth.js
    ├── !npm run build
    └── !git commit -m "feat(phase-1.3): create login endpoint"
```

### Validation Checklist
- [ ] **Git worktree created with issue name**
- [ ] **All work done in worktree directory**
- [ ] Each subphase has clear deliverable
- [ ] Lint/typecheck only new code
- [ ] Build passes before commit
- [ ] Commit message follows convention
- [ ] Documentation updated at phase end
- [ ] **NO merge to main branch**
- [ ] **NO push operations**
- [ ] No operations outside worktree

### Key Benefits
1. **Isolated Development**: Git worktree keeps work separate from main
2. **Incremental Progress**: Each subphase is independently committed
3. **Quality Assurance**: Automated checks before each commit
4. **Clean History**: Structured commit messages
5. **Focused Scope**: Only Phase 1 implementation
6. **Safe Operation**: No merge/push, stays in worktree
7. **Issue Tracking**: Worktree name matches issue for clarity