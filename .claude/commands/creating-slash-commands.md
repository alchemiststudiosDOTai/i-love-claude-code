# Creating Custom Slash Commands in Claude Code

This guide shows you how to create powerful custom slash commands to automate your development workflows.

## Quick Start (30 seconds)

```bash
# From your project root
mkdir -p .claude/commands
echo 'Deploy to production: $ARGUMENTS' > .claude/commands/deploy.md
```

That's it! Now you can use `/deploy` in Claude Code.

## How Slash Commands Work

Claude Code discovers commands automatically:
- **Project commands**: `.claude/commands/` (shared via Git)
- **Personal commands**: `~/.claude/commands/` (your machine only)
- **Format**: `/prefix:namespace:command` or simply `/command`

## Step-by-Step Guide

### 1. Create the Commands Directory

```bash
mkdir -p .claude/commands
```

### 2. Create Your Command File

Create a markdown file with your command name:

```bash
touch .claude/commands/my-command.md
```

### 3. Write Your Command

Basic template:

```markdown
# Command Title
Brief description of what this does

## Steps
1. First action
2. Second action
3. Final action

## Your task
$ARGUMENTS
```

### 4. Use Dynamic Features

- `$ARGUMENTS` - Captures everything after the command
- `!command` - Executes shell commands inline
- `@filename` - Includes file contents

Example with all features:

```markdown
# Deploy Command
Deploy the application to: $ARGUMENTS

## Current Status
!git status

## Deployment Steps
1. Run tests: !npm test
2. Build application: !npm run build
3. Deploy using config: @deploy-config.json
4. Verify deployment

Deploy to: $ARGUMENTS
```

## Practical Examples

### Test Runner Command

`.claude/commands/test.md`:
```markdown
Run tests for: $ARGUMENTS

1. Check test framework: !ls package.json
2. Run tests matching pattern: !npm test -- $ARGUMENTS
3. Generate coverage report if tests pass
```

### Code Review Command

`.claude/commands/review.md`:
```markdown
Review code changes for: $ARGUMENTS

## Analysis
1. Show changed files: !git diff --name-only
2. Check for common issues:
   - Security vulnerabilities
   - Performance problems
   - Code style violations
3. Suggest improvements

Focus area: $ARGUMENTS
```

### Database Migration Command

`.claude/commands/migrate.md`:
```markdown
Run database migration: $ARGUMENTS

## Pre-checks
- Database status: !npm run db:status
- Pending migrations: !npm run db:pending

## Execute
1. Backup current schema
2. Run migration: !npm run db:migrate $ARGUMENTS
3. Verify data integrity
```

## Advanced Features

### Namespaced Commands

Create subdirectories for namespaces:

```
.claude/commands/
├── frontend/
│   └── component.md    # Usage: /frontend:component
├── backend/
│   └── api.md         # Usage: /backend:api
└── deploy.md          # Usage: /deploy
```

### Command Metadata

Add YAML frontmatter for restrictions:

```markdown
---
description: Deploy to production
allowed-tools: Bash(git:*), Edit(*)
---

# Deploy Command
...
```

### Error Handling

Include error checks:

```markdown
# Safe Deploy
Deploy with safety checks

1. Check branch: !git branch --show-current
2. If not main, abort with error
3. Run full test suite: !npm test
4. If tests fail, abort deployment
5. Deploy only if all checks pass
```

## Best Practices

1. **Start Simple**: Basic commands first, add complexity later
2. **Use Clear Names**: `deploy-staging.md` not `ds.md`
3. **Include Context**: Always show current state with `!` commands
4. **Handle Errors**: Add checks and validation
5. **Document Well**: Clear steps and descriptions

## Common Patterns

### Git Workflow
```markdown
# Smart Commit
!git diff --cached
Analyze changes and create descriptive commit message
```

### Build & Deploy
```markdown
# Full Deploy
!npm test && npm run build && npm run deploy
Monitor each step and handle failures
```

### Code Generation
```markdown
# Generate Component
Create new component: $ARGUMENTS
Use existing patterns from: @src/components/
```

## Troubleshooting

**Command not found?**
- Check file is in `.claude/commands/`
- Filename must end with `.md`
- Restart Claude Code session

**Arguments not working?**
- Use `$ARGUMENTS` exactly (all caps)
- Place it where you want the input

**Commands failing?**
- Test shell commands manually first
- Check permissions with `/permissions`
- Use explicit paths in commands

## Tips for Power Users

1. **Chain Commands**: Reference other commands with `/command` syntax
2. **Share via Git**: Commit `.claude/commands/` for team use
3. **Personal Library**: Build your own command collection in `~/.claude/commands/`
4. **Template Everything**: Common tasks become one-command workflows

---

Remember: The best slash commands are the ones that save you time on repetitive tasks. Start with your most common workflows and expand from there.