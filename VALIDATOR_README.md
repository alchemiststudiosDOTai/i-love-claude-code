# Slash Command Validator

A Python tool to validate and enforce slash command requirements for Claude Code based on the official [slash.md](slash.md) documentation.

## Features

- ✅ **Frontmatter Validation**: Validates YAML frontmatter fields
- ✅ **Tool Permission Checking**: Ensures allowed-tools are properly configured
- ✅ **Argument Consistency**: Validates `$ARGUMENTS` and `$N` usage
- ✅ **Bash Command Detection**: Detects bash executions and validates permissions
- ✅ **File Reference Detection**: Identifies `@file` references
- ✅ **Extended Thinking Detection**: Identifies thinking mode usage
- ⚠️  **Detailed Warnings**: Provides helpful suggestions for improvements
- 📊 **Comprehensive Reports**: Clear, categorized validation results

## Installation

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows

# Install requirements
pip install -r requirements-validator.txt
```

### 2. Run the Validator

```bash
# Validate commands in default directory (./commands/)
python validate_commands.py

# Validate commands in a specific directory
python validate_commands.py /path/to/commands/
```

## Validation Rules

### Required Fields

- **description**: Recommended for `/help` listing (Warning if missing)

### Valid Frontmatter Fields

According to [slash.md](slash.md), these are the valid frontmatter fields:

| Field | Type | Description |
|-------|------|-------------|
| `allowed-tools` | String or List | Tools the command can use |
| `argument-hint` | String | Expected arguments (shown in autocomplete) |
| `description` | String | Brief command description |
| `model` | String | Specific Claude model to use |
| `disable-model-invocation` | Boolean | Prevent SlashCommand tool from calling this |

### Tool Validation

The validator checks that `allowed-tools` contains valid tool names:

- **Simple tools**: `Read`, `Write`, `Edit`, `View`, `Grep`, `Glob`, `Task`, `TodoWrite`, `WebFetch`, `WebSearch`
- **Bash tools**: `Bash(command:*)` format (e.g., `Bash(git:*)`, `Bash(npm:*)`)
- **MCP tools**: `mcp__server__tool` format
- **SlashCommand**: For invoking other slash commands

### Argument Validation

The validator ensures:

1. **Consistent argument style**: Don't mix `$ARGUMENTS` with positional args (`$1`, `$2`)
2. **Argument-hint presence**: If arguments are used, `argument-hint` should be defined
3. **Actual argument usage**: If `argument-hint` is defined, arguments should be used in content

### Bash Command Validation

When bash commands are detected with `!` prefix:

```markdown
!`git status`
```

The validator ensures:
- `Bash` or specific `Bash(command:*)` is in `allowed-tools`

## Common Issues and Fixes

### Issue 1: Square Brackets in argument-hint

**Problem**: YAML interprets square brackets as arrays

```yaml
# ❌ INVALID - YAML parsing error
argument-hint: [artifact-path] [description]
```

**Fix**: Quote the entire value

```yaml
# ✅ VALID
argument-hint: "[artifact-path] [description]"
```

### Issue 2: Missing description

**Problem**: No description field in frontmatter

**Fix**: Add a clear, concise description

```yaml
---
description: Brief description of what this command does
---
```

### Issue 3: Bash commands without permission

**Problem**: Using `!`git status`` without Bash in allowed-tools

**Fix**: Add Bash to allowed-tools

```yaml
---
allowed-tools: Read, View, Bash(git:*)
---
```

### Issue 4: Argument-hint without arguments

**Problem**: Defined `argument-hint` but never use `$ARGUMENTS` or `$1`, `$2`, etc.

**Fix**: Either use the arguments or remove the hint

```markdown
# Option 1: Use arguments
Process issue: $ARGUMENTS

# Option 2: Remove argument-hint if not needed
```

### Issue 5: Mixed argument styles

**Problem**: Using both `$ARGUMENTS` and positional args

```markdown
# ❌ Don't mix styles
Process $ARGUMENTS for issue $1
```

**Fix**: Choose one style

```markdown
# ✅ Use $ARGUMENTS for all args
Process $ARGUMENTS

# ✅ OR use positional args
Process issue $1 with priority $2
```

## Validation Output

The validator produces three categories:

### ❌ Invalid Files
Files with errors that prevent them from working correctly:
- YAML parsing errors
- Empty required fields
- Permission mismatches

### ⚠️ Valid Files with Warnings
Files that work but could be improved:
- Missing recommended fields
- Unused argument hints
- Long descriptions

### ✅ Fully Valid Files
Files that pass all validation without warnings

## Exit Codes

- `0`: All files valid (warnings are OK)
- `1`: One or more files have errors

## Integration with CI/CD

Add to your GitHub Actions workflow:

```yaml
name: Validate Slash Commands

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements-validator.txt
      - name: Validate commands
        run: |
          python validate_commands.py commands/
```

## Best Practices

1. **Always quote values with special characters** in YAML frontmatter
2. **Keep descriptions under 200 characters** for better readability
3. **Use specific Bash permissions** instead of blanket `Bash` access
4. **Document expected arguments** with `argument-hint`
5. **Be consistent** with argument style (`$ARGUMENTS` vs `$1`, `$2`)
6. **Test your commands** after making changes
7. **Run the validator** before committing changes

## Examples

### Minimal Valid Command

```markdown
---
description: Simple command example
---

# Simple Command

This is a simple slash command that doesn't need any special tools.
```

### Command with Arguments

```markdown
---
description: Process GitHub issue
argument-hint: "[issue-number]"
allowed-tools: Bash(gh:*), View
---

# Process Issue

Process GitHub issue #$ARGUMENTS

Current issue details: !`gh issue view $ARGUMENTS`
```

### Command with Multiple Tools

```markdown
---
description: Research and document findings
argument-hint: "[topic]"
allowed-tools: Read, View, Grep, Glob, Task, TodoWrite
---

# Research Topic

Research the following topic: $ARGUMENTS

This command will search the codebase and document findings.
```

## Troubleshooting

### Python Dependency Errors

If you see "module not found" errors:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements-validator.txt
```

### YAML Parsing Errors

If you see YAML parsing errors:
1. Check for unquoted special characters: `[]`, `{}`, `:`, `-`, `|`
2. Ensure proper indentation (use spaces, not tabs)
3. Quote any value that starts with special characters

### Validator Not Finding Files

Make sure:
1. You're running from the correct directory
2. The path to commands/ is correct
3. Files have `.md` extension
4. Files are not named `README.md` (excluded by design)

## Contributing

When adding new validation rules:

1. Update `VALID_FRONTMATTER_FIELDS` for new frontmatter fields
2. Update `VALID_MODELS` when new Claude models are released
3. Update `TOOL_PATTERNS` for new tool types
4. Add tests for the new validation rules
5. Update this README with examples

## License

This validator is part of the i-love-claude-code documentation repository.

## See Also

- [slash.md](slash.md) - Official slash command documentation
- [commands/README.md](commands/README.md) - Command examples and guides
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
