# How to Create Slash Commands

A comprehensive guide to creating custom slash commands for Claude Code.

## Table of Contents

1. [What are Slash Commands?](#what-are-slash-commands)
2. [Minimum Requirements](#minimum-requirements)
3. [File Structure](#file-structure)
4. [Frontmatter Fields](#frontmatter-fields)
5. [Command Content](#command-content)
6. [Best Practices](#best-practices)
7. [Examples](#examples)
8. [Testing & Validation](#testing--validation)

---

## What are Slash Commands?

Slash commands are custom markdown files that extend Claude Code's capabilities. When you type `/command-name`, Claude Code loads the markdown file and uses it as additional instructions.

**Key Benefits:**
- 🚀 Automate repetitive workflows
- 📋 Standardize team processes
- 🎯 Create domain-specific assistants
- 🔧 Customize Claude's behavior per-task

---

## Minimum Requirements

At the absolute minimum, a slash command needs:

1. **A markdown file** with `.md` extension
2. **YAML frontmatter** (even if empty)
3. **Some content** explaining what the command does

### Minimal Valid Example

```markdown
---
description: Simple example command
---

# My First Command

This command does something helpful.
```

That's it! This is a fully functional slash command.

---

## File Structure

### Location

Place your slash command files in:
- `.claude/commands/` - Project-specific commands
- `~/.config/claude/commands/` - Global commands (all projects)

### Naming Convention

- **Filename becomes the command name**
  - `my-command.md` → `/my-command`
  - `api-docs.md` → `/api-docs`
- Use **kebab-case** (lowercase with hyphens)
- Avoid spaces and special characters
- Be descriptive but concise

### Subdirectories

You can organize commands in subdirectories:
```
commands/
  ├── README.md
  ├── api/
  │   ├── create-endpoint.md
  │   └── test-endpoint.md
  └── docker/
      └── optimize.md
```

Commands are still invoked by filename only: `/create-endpoint`

---

## Frontmatter Fields

Frontmatter is YAML metadata at the top of your file, enclosed by `---`:

```yaml
---
description: Brief description of what this command does
allowed-tools: Read, Write, Bash(git:*)
argument-hint: "[arg1] [arg2]"
model: claude-sonnet-4-5-20250929
disable-model-invocation: false
---
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | String | **Recommended** | Shown in `/help` listing (keep under 200 chars) |
| `allowed-tools` | String/List | Optional | Tools this command can use |
| `argument-hint` | String | Optional | Expected arguments (shown in autocomplete) |
| `model` | String | Optional | Specific Claude model to use |
| `disable-model-invocation` | Boolean | Optional | Prevent SlashCommand tool from calling this |

### `description`

**Best practices:**
- Keep it under 200 characters
- Be specific about what the command does
- Use action verbs (e.g., "Generate", "Analyze", "Fix")

```yaml
# ✅ Good
description: Generate API endpoint with tests and documentation

# ❌ Too vague
description: Does stuff with APIs

# ❌ Too long
description: This command will help you generate a complete REST API endpoint including the route handler, request validation, database integration, error handling, unit tests, integration tests, and comprehensive documentation
```

### `allowed-tools`

Specify which tools the command can use. This is a security feature.

**Available tools:**
- `Read` - Read files
- `Write` - Write files
- `Edit` - Edit files
- `View` - View files (read-only)
- `Grep` - Search file contents
- `Glob` - Find files by pattern
- `Task` - Spawn sub-agents
- `TodoWrite` - Manage todo lists
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- `Bash(command:*)` - Execute specific bash commands
- `SlashCommand` - Invoke other slash commands
- `mcp__*` - MCP server tools

**Format options:**

```yaml
# String format (comma-separated)
allowed-tools: Read, Write, Edit

# List format
allowed-tools:
  - Read
  - Write
  - Edit

# Specific bash commands
allowed-tools: Read, Bash(git:*), Bash(npm:*)

# All bash commands (use carefully!)
allowed-tools: Read, Bash
```

**⚠️ Security note:** Only grant the minimum tools needed. Bash access should be specific:
- ✅ `Bash(git:*)` - Only git commands
- ❌ `Bash` - All bash commands (risky!)

### `argument-hint`

Shows expected arguments in autocomplete and help.

```yaml
# Single argument
argument-hint: "[file-path]"

# Multiple arguments
argument-hint: "[component-name] [output-dir]"

# Optional arguments
argument-hint: "[issue-number] [optional-branch-name]"
```

**⚠️ YAML gotcha:** Quote values with square brackets!

```yaml
# ❌ WRONG - YAML parsing error
argument-hint: [file-path]

# ✅ CORRECT
argument-hint: "[file-path]"
```

### `model`

Force a specific Claude model for this command.

```yaml
# Latest Sonnet (best for complex tasks)
model: claude-sonnet-4-5-20250929

# Haiku (fast, cost-effective for simple tasks)
model: claude-3-5-haiku-20241022

# Opus (maximum capability)
model: claude-opus-4-20250514
```

**When to specify a model:**
- **Haiku**: Simple, fast operations (formatting, simple transforms)
- **Sonnet**: Most commands (default is usually fine)
- **Opus**: Complex reasoning, critical decisions

### `disable-model-invocation`

Prevents the SlashCommand tool from invoking this command recursively.

```yaml
disable-model-invocation: true
```

Use this for meta-commands that orchestrate other commands.

---

## Command Content

After the frontmatter, write your command instructions in markdown.

### Using Arguments

Access user arguments with special variables:

```markdown
# Using $ARGUMENTS (all arguments as one string)
Process the following file: $ARGUMENTS

# Using positional arguments
Component name: $1
Output directory: $2
Optional flag: $3
```

**⚠️ Don't mix styles!** Use either `$ARGUMENTS` OR `$1, $2, $3` - not both.

### File References

Reference files with `@` prefix:

```markdown
Check the configuration in @config/settings.json
Review the implementation in @src/components/Button.tsx
```

### Bash Command Execution

Execute bash commands inline with `!` prefix:

```markdown
Current git status: !`git status`
List issues: !`gh issue list --limit 5`
```

**⚠️ Important:**
- Must have `Bash` or `Bash(command:*)` in `allowed-tools`
- Commands run in the project directory
- Output is captured and shown to Claude

### Extended Thinking

Use thinking modes for complex tasks:

```markdown
<ultrathink>
This is a complex refactoring task requiring careful analysis
of dependencies and potential side effects...
</ultrathink>

<megaexpertise type="database-optimization-specialist">
The assistant should analyze query performance and suggest
indexes, query rewrites, and schema improvements.
</megaexpertise>
```

### Sections and Structure

Organize your command with clear sections:

```markdown
## Context Gathering
<!-- What information to collect first -->

## Planning Phase
<!-- How to approach the task -->

## Implementation Steps
<!-- Step-by-step execution -->

## Validation
<!-- How to verify success -->

## Success Criteria
<!-- What defines completion -->
```

---

## Best Practices

### 1. Keep Commands Focused

**Do:**
```markdown
# ✅ create-api-endpoint.md
Generate a REST API endpoint with validation and tests
```

**Don't:**
```markdown
# ❌ do-everything.md
Create APIs, fix bugs, write docs, and make coffee
```

### 2. Be Explicit About Steps

```markdown
## Steps

1. **Read existing routes**
   - Check @src/routes/ for similar patterns
   - Validation: !`ls src/routes/`

2. **Create endpoint file**
   - Generate route handler in src/routes/$1.ts
   - Include request validation

3. **Write tests**
   - Create test file in tests/routes/$1.test.ts
   - Cover happy path and error cases
```

### 3. Include Validation Checks

Help Claude verify work at each step:

```markdown
### Validation
- File created: !`test -f src/routes/$1.ts && echo "✓" || echo "✗"`
- Tests passing: !`npm test -- $1.test.ts`
- Lint clean: !`npm run lint src/routes/$1.ts`
```

### 4. Document Expected Arguments

```markdown
# Create API Endpoint

**Usage:** `/create-api-endpoint [endpoint-name] [http-method]`

**Example:** `/create-api-endpoint users GET`

Creates: $ARGUMENTS endpoint at src/routes/$1.ts using $2 method
```

### 5. Provide Context

```markdown
## Context
This command follows our team's API conventions:
- RESTful routing: @docs/api-conventions.md
- Validation with Zod: @src/lib/validation.ts
- Testing with Vitest: @tests/setup.ts
```

### 6. Handle Edge Cases

```markdown
## Error Handling

If route already exists:
- Check: !`test -f src/routes/$1.ts`
- Ask user whether to overwrite or choose new name
- Don't silently overwrite!
```

### 7. Keep Descriptions Concise

```yaml
# ✅ Good (78 chars)
description: Create REST endpoint with validation, error handling, and tests

# ❌ Too long (215 chars)
description: This comprehensive command will generate a complete REST API endpoint including route handlers, request/response validation using Zod schemas, proper error handling middleware, unit tests, integration tests, and documentation
```

### 8. Version Control Friendly

Include git operations when appropriate:

```markdown
## Finalization

1. Review changes: !`git diff`
2. Stage files: !`git add src/routes/$1.ts tests/routes/$1.test.ts`
3. Suggest commit message: "feat: Add $1 endpoint"
```

### 9. Test Your Commands

Before sharing:
```bash
# 1. Validate syntax
python validate_commands.py commands/

# 2. Test the command
/your-command test-arg

# 3. Check with different arguments
/your-command edge-case
```

### 10. Document Dependencies

```markdown
## Prerequisites
- Node.js 18+
- GitHub CLI installed: !`gh --version`
- Authenticated: !`gh auth status`
```

---

## Examples

### Example 1: Minimal Command

**File:** `commands/hello.md`

```markdown
---
description: Simple greeting command
---

# Hello Command

Hello! This is a minimal slash command example.

You provided: $ARGUMENTS
```

**Usage:** `/hello world` → "You provided: world"

---

### Example 2: File Operation Command

**File:** `commands/create-component.md`

```markdown
---
description: Create React component with TypeScript
allowed-tools: Read, Write, View
argument-hint: "[component-name]"
---

# Create React Component

Creating component: $ARGUMENTS

## Steps

1. Read existing component pattern: @src/components/Button.tsx
2. Generate $ARGUMENTS.tsx in src/components/
3. Generate $ARGUMENTS.test.tsx in tests/components/

## Component Template

\`\`\`tsx
interface ${ARGUMENTS}Props {
  children: React.ReactNode
}

export function $ARGUMENTS({ children }: ${ARGUMENTS}Props) {
  return <div>{children}</div>
}
\`\`\`

## Success Criteria
- ✓ Component file created
- ✓ Test file created
- ✓ Exports added to index.ts
```

---

### Example 3: Git Workflow Command

**File:** `commands/pr-create.md`

```markdown
---
description: Create pull request with description from commits
allowed-tools: View, Bash(git:*), Bash(gh:*)
---

# Create Pull Request

## Context Gathering

- Current branch: !`git branch --show-current`
- Commits since main: !`git log main..HEAD --oneline`
- Changed files: !`git diff main --stat`

## Generate PR Description

Create PR description summarizing:
1. What changed (from commit messages)
2. Why (from commit bodies)
3. Testing done

## Create PR

Run: !`gh pr create --title "..." --body "..."`

## Validation

- PR created: !`gh pr view`
- CI passing: !`gh pr checks`
```

---

### Example 4: Research Command

**File:** `commands/explain-code.md`

```markdown
---
description: Explain how code works with examples
allowed-tools: Read, Grep, View
argument-hint: "[file-path-or-pattern]"
---

# Explain Code

Analyzing: $ARGUMENTS

## Investigation

1. **Read the code:** @$ARGUMENTS

2. **Find usage examples:**
   - Search for imports: Search codebase for `from '$ARGUMENTS'`
   - Find tests: Look in tests/ directory

3. **Understand context:**
   - Check related files
   - Review documentation

## Explanation

Provide:
- **What it does:** High-level purpose
- **How it works:** Key algorithms/patterns
- **Usage examples:** Real code from the project
- **Dependencies:** What it relies on
- **Testing:** How it's tested

Keep explanation clear and example-driven.
```

---

### Example 5: Multi-Phase Command

**File:** `commands/refactor-function.md`

```markdown
---
description: Refactor function with tests and validation
allowed-tools: Read, Edit, View, Bash(npm:test)
argument-hint: "[file-path] [function-name]"
model: claude-sonnet-4-5-20250929
---

# Refactor Function

Refactoring: $2 in @$1

## Phase 1: Understanding

1. Read current implementation: @$1
2. Find tests: Search for test files referencing $2
3. Find usage: Search codebase for calls to $2

## Phase 2: Analysis

<ultrathink>
Analyze the function for:
- Complexity (cyclomatic complexity)
- Readability issues
- Performance concerns
- Type safety
- Test coverage gaps
</ultrathink>

## Phase 3: Planning

Create refactoring plan:
1. What to improve (specific issues)
2. How to improve (techniques)
3. How to verify (tests)

**Get user approval before proceeding.**

## Phase 4: Implementation

1. Update function in @$1
2. Update/add tests
3. Update documentation

## Phase 5: Validation

- Tests pass: !`npm test -- $1`
- Lint clean: !`npm run lint $1`
- Type check: !`npm run type-check`
- No breaking changes in callers

## Success Criteria

- ✓ Function improved (measurable: less complex, more readable)
- ✓ All tests passing
- ✓ No breaking changes
- ✓ Documentation updated
```

---

## Testing & Validation

### Use the Validator

Always validate your commands before committing:

```bash
# Validate all commands
python validate_commands.py commands/

# Auto-fix common issues
python fix_commands.py commands/ --dry-run
python fix_commands.py commands/
```

### Manual Testing Checklist

- [ ] Command loads without errors
- [ ] Arguments are processed correctly
- [ ] File references work (`@file`)
- [ ] Bash commands execute (if used)
- [ ] Output is helpful and actionable
- [ ] Edge cases handled
- [ ] Success criteria clear

### Common Issues

**Issue:** Command not found
```bash
# Check file location
ls -la .claude/commands/your-command.md

# Verify Claude can see it
/help | grep your-command
```

**Issue:** YAML parsing error
```yaml
# ❌ Unquoted special characters
argument-hint: [file]

# ✅ Quote them
argument-hint: "[file]"
```

**Issue:** Bash commands fail
```yaml
# Ensure Bash permission granted
allowed-tools: Bash(git:*)
```

**Issue:** Arguments not working
```markdown
# Don't mix styles
❌ Process $ARGUMENTS in file $1

# Use one or the other
✅ Process $ARGUMENTS
✅ Process file $1
```

---

## Advanced Topics

### Spawning Sub-Agents

Use the Task tool for complex, multi-step operations:

```markdown
---
allowed-tools: Task, TodoWrite
---

# Complex Research Task

## Phase 1: Spawn Research Agents

Launch 3 parallel research agents:
1. Codebase locator: Find relevant files
2. Implementation analyzer: Understand how it works
3. Usage finder: Find all usage examples

Wait for all agents to complete.

## Phase 2: Synthesize Findings

Combine results from all agents into coherent explanation.
```

### Chaining Commands

```markdown
# Command 1: Research
---
description: Research codebase for patterns
---
Document findings in research.md

# Command 2: Plan
---
description: Create implementation plan from research
---
Read @research.md and create plan.md

# Command 3: Execute
---
description: Implement based on plan
---
Follow steps in @plan.md
```

User invokes: `/research` → `/plan` → `/execute`

### Dynamic Context

```markdown
## Context-Aware Behavior

Check project type:
- If package.json exists: Node.js project
- If requirements.txt exists: Python project
- If go.mod exists: Go project

Adapt command behavior accordingly.
```

---

## Resources

- **Validation Tools:**
  - [validate_commands.py](../validate_commands.py) - Validate command syntax
  - [fix_commands.py](../fix_commands.py) - Auto-fix common issues

- **Documentation:**
  - [VALIDATOR_README.md](../VALIDATOR_README.md) - Full validator docs
  - [slash.md](../slash.md) - Slash command reference
  - [Official Claude Code Docs](https://docs.claude.com/en/docs/claude-code)

- **Examples:**
  - Browse [commands/](.) directory for production examples
  - [context engineering/](context%20engineering/) - Advanced workflow examples

---

## Quick Reference

### Command Template

```markdown
---
description: Brief description (under 200 chars)
allowed-tools: Read, Write, Edit
argument-hint: "[arg1] [arg2]"
---

# Command Name

Brief introduction: $ARGUMENTS

## Context
What to gather first

## Steps
1. First step
2. Second step

## Validation
How to verify success

## Success Criteria
- ✓ Criterion 1
- ✓ Criterion 2
```

### Validation Command

```bash
python validate_commands.py commands/
```

### Common Patterns

- Arguments: `$ARGUMENTS` or `$1, $2, $3`
- File refs: `@path/to/file`
- Bash exec: `!`git status``
- Thinking: `<ultrathink>...</ultrathink>`

---

**Happy commanding! 🚀**

For questions or issues, see the main [README.md](../README.md) or submit an issue.
