<!-- 
CRITICAL: Keep CLAUDE.md under 150 lines!
Past 200 lines, Claude starts ignoring instructions.
Be DIRECT. Use STRONG language. Less is more.

Structure:
1. Small project map
2. Clear workflow outline  
3. Bash/CLI/MCP commands embedded
4. Style/format rules
-->

# CLAUDE.md Example

## Project Map
```
src/
├── api/        # REST endpoints
├── core/       # Business logic
├── utils/      # Shared utilities
└── tests/      # Test suite
```

## Critical Instructions

### 1. ALWAYS Start With Context
- **STOP** - Read existing code before writing anything
- **SEARCH** first, code second
- **NEVER** assume libraries exist - check package.json/requirements.txt

### 2. Git Workflow 
```bash
# BEFORE any changes
git add . && git commit -m "checkpoint: before [task]"

# AFTER completion
git add . && git commit -m "feat/fix: [what changed]"
```

### 3. Testing Protocol
**MANDATORY**: Write test FIRST, code SECOND
```bash
# Run tests - adjust command per project
npm test          # Node.js
pytest            # Python
cargo test        # Rust
```

### 4. Code Standards

#### JavaScript/TypeScript
- **USE** async/await, not callbacks
- **USE** const/let, never var
- **RUN** `npm run lint` after EVERY file change

#### Python
- **USE** type hints ALWAYS
- **USE** pathlib, not os.path
- **RUN** `ruff check .` frequently

#### General
- **MATCH** existing code style EXACTLY
- **NO** comments unless fixing bugs
- **NO** console.log/print in production code

### 5. Documentation Updates
After significant changes:
```bash
# Update project docs
echo "## Changes\n- [what changed]\n- [why]" >> docs/CHANGES.md
```

### 6. MCP Tools Available
```bash
# Use these via MCP when available
task-manager     # For complex multi-step tasks
git-helper       # For advanced git operations
test-runner      # For test automation
```

### 7. Error Handling
- **NEVER** swallow errors silently
- **ALWAYS** log errors with context
- **STOP** and ask user if unsure

### 8. File Operations
- **EDIT** existing files, don't create new ones
- **CHECK** file exists before reading/writing
- **USE** proper file paths (absolute when needed)

### 9. Security Rules
- **NEVER** commit secrets/keys
- **NEVER** log sensitive data
- **VALIDATE** all user inputs

### 10. Performance
- **AVOID** nested loops when possible
- **USE** built-in methods over custom implementations
- **PROFILE** before optimizing

## Workflow Checklist

1. □ Understand task completely
2. □ Search codebase for context
3. □ Create git checkpoint
4. □ Write/find test first
5. □ Implement solution
6. □ Run tests
7. □ Run linter
8. □ Commit with clear message
9. □ Update docs if needed

## Common Commands
```bash
# Development
npm run dev       # Start dev server
npm run build     # Build project
npm run lint      # Check code style
npm test          # Run tests

# Git
git status        # Check changes
git diff          # View changes
git log --oneline # Recent commits
gh pr create      # Create pull request

# Search
grep -r "pattern" src/    # Find in files
find . -name "*.js"       # Find files
```

## CRITICAL REMINDERS

**STOP means STOP** - Don't proceed without clarity
**TEST FIRST** - No exceptions
**LINT ALWAYS** - Before committing
**ASK IF UNSURE** - User prefers questions over mistakes

---
