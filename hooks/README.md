# Claude Code Hooks

This directory contains hooks organized by category.

## Directory Structure

```
hooks/
├── security/                # Security validation hooks
│   └── security-validator.py
├── formatting/              # Code formatting hooks
│   └── auto-formatter.sh
├── notification/            # Notification hooks
├── README.md                # This file
```

## Categories

### [security/](security/)
Hooks for validating and securing operations:
- `security-validator.py` - Validates file access and blocks dangerous operations

### [formatting/](formatting/)
Hooks for automatic code formatting:
- `auto-formatter.sh` - Formats code after edits

### [notification/](notification/)
Hooks for notifications (directory ready for future hooks)

## Using Hooks

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/security/security-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/formatting/auto-formatter.sh"
          }
        ]
      }
    ]
  }
}
```

## Hook Events

- **PreToolUse** - Runs before a tool executes, can block operations
- **PostToolUse** - Runs after a tool completes successfully
- **UserPromptSubmit** - Runs when you submit a prompt
- **SessionStart** - Runs when Claude Code starts
- **Notification** - Runs when Claude needs to notify you
- **Stop/SubagentStop** - Runs when Claude stops
- **PreCompact** - Runs before context compaction
