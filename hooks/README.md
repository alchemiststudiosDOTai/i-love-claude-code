# Claude Code Hooks: Order for ai agents

Claude Code hooks are user-defined shell commands that execute automatically at specific points in Claude Code's lifecycle, providing deterministic control over the AI assistant's behavior. Unlike relying on prompts that Claude might forget or interpret differently, hooks ensure certain actions always happen—from formatting code after edits to blocking dangerous operations before they execute. This comprehensive guide covers the complete hook system, implementation patterns, best practices, and real-world examples that will help you build a fully automated development workflow tailored to your needs.

## Understanding the hook lifecycle and event system

Claude Code provides eight distinct hook events that fire at critical moments during operation. Each event serves a specific purpose and offers different levels of control over Claude's behavior.

**PreToolUse** fires after Claude creates tool parameters but before processing the tool call. This hook can block operations entirely, making it ideal for security validation, permission control, and input sanitization. It supports matchers for specific tools like `Edit`, `Write`, `Bash`, or patterns like `Edit|MultiEdit|Write`. When a hook returns exit code 2 or a JSON response with `decision: "block"`, Claude receives the error message and attempts to correct its approach.

**PostToolUse** runs immediately after a tool completes successfully, perfect for automatic code formatting, running tests, or logging operations. While it can provide feedback to Claude through blocking errors, its primary use is for cleanup and quality assurance tasks that should happen after every file modification or command execution.

**UserPromptSubmit** executes when you submit a prompt, before Claude processes it. This powerful hook can inject additional context, validate prompts for security, or log all interactions. Uniquely, its stdout output gets added to Claude's context, allowing you to dynamically enhance prompts with current git status, recent issues, or project-specific information.

**SessionStart** fires when Claude Code starts a new session or resumes an existing one. Like UserPromptSubmit, its stdout becomes part of Claude's context, making it ideal for loading development context, initializing environment variables, or setting up project-specific configurations. The hook receives a `source` parameter indicating whether it's a fresh startup, resume, or clear operation.

**Notification** triggers whenever Claude Code needs to notify you about something—waiting for input, requesting permissions, or reporting status. While it can't block Claude's operation, it's perfect for custom desktop alerts, mobile notifications through services like ntfy, or text-to-speech announcements that grab your attention when Claude needs you.

**Stop** and **SubagentStop** run when Claude or its subagents finish responding. These hooks can actually prevent Claude from stopping by returning a blocking decision, forcing it to continue working based on your criteria. Common uses include enforcing test passage before completion, automated follow-up actions, or cleanup tasks.

**PreCompact** executes before Claude performs context compaction to manage token limits. While it can't block the operation, it's valuable for backing up conversation transcripts, preserving important context, or logging what information Claude is about to forget.

## Configuration architecture and syntax patterns

Hooks are configured through a hierarchical settings system that allows both project-specific and user-wide configurations. The system checks three locations in order: `~/.claude/settings.json` for user-wide settings, `.claude/settings.json` for project-specific hooks that should be version controlled, and `.claude/settings.local.json` for local overrides that won't be committed.

The basic configuration structure uses a JSON format that maps event names to arrays of hook configurations. For events that support matchers (PreToolUse and PostToolUse), you can target specific tools using exact matches, regex patterns, or wildcards. Events without matchers run for all occurrences.

Here's a comprehensive configuration example that demonstrates multiple patterns:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/validate_file_access.py",
            "timeout": 30
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/validate_command.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_FILE_PATHS\" =~ \\.py$ ]]; then black \"$CLAUDE_FILE_PATHS\"; fi"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/enhance_prompt.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' \"$CLAUDE_NOTIFICATION\""
          }
        ]
      }
    ]
  }
}
```

Matcher patterns for PreToolUse and PostToolUse are case-sensitive and support several formats. Exact matches like `"Write"` target only that specific tool. Regex patterns like `"Edit|MultiEdit|Write"` or `"Notebook.*"` match multiple tools. Wildcards using `"*"` or empty string `""` match all tools. For MCP tools, use patterns like `"mcp__github__.*"` to target specific integrations.

## Communication protocols and control mechanisms

Hooks communicate with Claude Code through exit codes and structured JSON output, providing sophisticated control over execution flow. The communication protocol uses three primary exit codes with specific behaviors.

Exit code 0 indicates success. For most hooks, stdout is shown to the user in transcript mode. However, UserPromptSubmit and SessionStart hooks have special behavior where stdout gets injected into Claude's context, allowing dynamic prompt enhancement.

Exit code 2 triggers a blocking error. The stderr output is automatically fed back to Claude as feedback, causing it to reconsider its approach. This is the primary mechanism for preventing dangerous operations or enforcing constraints.

Any other exit code represents a non-blocking error. The stderr is shown to the user, but execution continues normally. This is useful for warnings or non-critical issues.

For more sophisticated control, hooks can output structured JSON that Claude Code interprets. The JSON response system allows fine-grained control over continuation, user feedback, and Claude's behavior:

```json
{
  "continue": false,
  "stopReason": "Security policy prevents modifying system files",
  "suppressOutput": true,
  "decision": "block",
  "reason": "Attempting to modify /etc/passwd is not allowed"
}
```

Different events support specific JSON fields for advanced control. PreToolUse hooks can return permission decisions:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Production database access requires manual approval"
  }
}
```

UserPromptSubmit and SessionStart can inject additional context:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Current sprint goals:\n1. Fix authentication bug\n2. Implement user dashboard\n\nRecent commits:\n- Fixed memory leak in worker process\n- Updated dependencies"
  }
}
```

## Security implementation and safety patterns

Security must be the primary consideration when implementing hooks, as they execute with your full user permissions. Never trust input data from Claude without validation, always use proper shell escaping, and implement defense in depth.

A robust security validation pattern for PreToolUse hooks blocks dangerous operations before they can cause harm:

```python
#!/usr/bin/env python3
import json
import sys
import re

# Load the hook payload
data = json.load(sys.stdin)
tool_name = data.get('tool_name', '')
tool_input = data.get('tool_input', {})

# Security checks for file operations
if tool_name in ['Edit', 'Write', 'MultiEdit']:
    file_path = tool_input.get('file_path', '')
    
    # Block sensitive files
    sensitive_patterns = ['.env', '.git/', 'id_rsa', '/etc/', '~/.ssh/']
    if any(pattern in file_path for pattern in sensitive_patterns):
        print(f"Access denied: {file_path} matches sensitive pattern", file=sys.stderr)
        sys.exit(2)
    
    # Prevent path traversal
    if '..' in file_path:
        print("Path traversal detected", file=sys.stderr)
        sys.exit(2)

# Security checks for shell commands
elif tool_name == 'Bash':
    command = tool_input.get('command', '')
    
    # Block dangerous commands
    dangerous_patterns = [
        r'rm\s+.*-[rf]',          # rm -rf variants
        r'sudo\s+rm',             # sudo rm commands
        r'chmod\s+777',           # Dangerous permissions
        r'>\s*/etc/',             # Writing to system directories
        r'curl.*\|.*bash',        # Pipe curl to bash
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            response = {
                "decision": "block",
                "reason": f"Command matches dangerous pattern: {pattern}"
            }
            print(json.dumps(response))
            sys.exit(0)

# Allow all other operations
sys.exit(0)
```

The hook configuration system itself includes security features. Direct edits to settings files don't take effect immediately—Claude Code captures hook snapshots at startup, preventing malicious runtime modifications. Changes require review through the `/hooks` command interface to apply.

## Practical implementation patterns

Real-world hook implementations follow several proven patterns that address common development needs. These patterns, refined by the community, provide templates for building your own automation.

**Automatic code formatting** ensures consistent style without manual intervention. This PostToolUse hook runs appropriate formatters based on file type:

```bash
#!/bin/bash
for file in $CLAUDE_FILE_PATHS; do
    case "$file" in
        *.py)
            black "$file" && ruff check --fix "$file"
            ;;
        *.js|*.jsx|*.ts|*.tsx)
            prettier --write "$file"
            eslint --fix "$file"
            ;;
        *.go)
            gofmt -w "$file"
            ;;
        *.rs)
            rustfmt "$file"
            ;;
    esac
done
```

**Test-driven development integration** automatically runs tests after code changes, ensuring Claude's modifications don't break existing functionality:

```python
#!/usr/bin/env python3
import subprocess
import json
import sys

# Run tests based on changed files
data = json.load(sys.stdin)
file_paths = data.get('tool_input', {}).get('file_path', '')

if file_paths.endswith('.py'):
    # Find and run related tests
    test_file = file_paths.replace('/src/', '/tests/test_')
    result = subprocess.run(['pytest', test_file, '-v'], capture_output=True)
    
    if result.returncode != 0:
        # Tests failed - inform Claude
        response = {
            "decision": "block",
            "reason": f"Tests failed:\n{result.stdout.decode()}\nPlease fix the failing tests."
        }
        print(json.dumps(response))
```

**Smart notification systems** provide context-aware alerts that grab your attention when needed:

```python
#!/usr/bin/env python3
import json
import sys
import subprocess
from datetime import datetime

data = json.load(sys.stdin)
message = data.get('message', '')

# Determine notification urgency
urgent_keywords = ['error', 'failed', 'permission', 'waiting for approval']
is_urgent = any(keyword in message.lower() for keyword in urgent_keywords)

# Multi-channel notification
if is_urgent:
    # Desktop notification
    subprocess.run(['notify-send', '-u', 'critical', 'Claude Code Alert', message])
    
    # Text-to-speech for urgent messages
    subprocess.run(['say', f"Claude needs your attention: {message[:50]}"])
    
    # Mobile notification via ntfy
    subprocess.run(['curl', '-d', message, 'ntfy.sh/my-claude-alerts'])
else:
    # Simple desktop notification for non-urgent
    subprocess.run(['notify-send', 'Claude Code', message])
```

## Advanced automation workflows

Complex development workflows benefit from sophisticated hook orchestration that coordinates multiple events to create seamless automation.

**Context-aware development sessions** use SessionStart and UserPromptSubmit hooks to maintain rich context throughout your work:

```python
#!/usr/bin/env python3
# SessionStart hook that loads comprehensive context
import subprocess
import json
from pathlib import Path

def load_development_context():
    context_parts = []
    
    # Git status and recent commits
    git_status = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
    recent_commits = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                  capture_output=True, text=True)
    
    context_parts.append(f"Git Status:\n{git_status.stdout}")
    context_parts.append(f"Recent Commits:\n{recent_commits.stdout}")
    
    # Load project-specific context files
    context_files = ['.claude/context.md', 'TODO.md', '.claude/current_task.md']
    for file in context_files:
        if Path(file).exists():
            with open(file) as f:
                context_parts.append(f"{file}:\n{f.read()}")
    
    # Current GitHub issues
    issues = subprocess.run(['gh', 'issue', 'list', '--limit', '5', '--json', 
                           'title,number,labels'], capture_output=True, text=True)
    if issues.returncode == 0:
        context_parts.append(f"Open Issues:\n{issues.stdout}")
    
    # Output context for Claude
    print("\n---\n".join(context_parts))

if __name__ == "__main__":
    load_development_context()
```

**Multi-agent observability systems** provide real-time monitoring of Claude's activities across multiple sessions. This advanced pattern uses hooks to stream events to a central server:

```python
#!/usr/bin/env python3
# Universal hook logger for observability
import json
import sys
import requests
from datetime import datetime

# Load hook data
data = json.load(sys.stdin)
event_name = data.get('hook_event_name', 'unknown')
session_id = data.get('session_id', 'unknown')

# Prepare event for logging
event = {
    'timestamp': datetime.utcnow().isoformat(),
    'session_id': session_id,
    'event_type': event_name,
    'tool_name': data.get('tool_name'),
    'payload': data
}

# Stream to observability server
try:
    requests.post('http://localhost:8080/events', json=event, timeout=1)
except:
    pass  # Don't block Claude if logging fails

# Continue normal execution
sys.exit(0)
```

## Troubleshooting guide and solutions

Common issues with hooks often stem from path resolution, permissions, or configuration problems. Understanding these patterns helps quickly resolve issues.

**Hook scripts not executing** usually indicates permission or path problems. Ensure scripts are executable with `chmod +x`, use absolute paths or the `$CLAUDE_PROJECT_DIR` variable, and verify JSON syntax in settings files. The UV (uv) tool provides excellent script portability:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["requests", "python-dotenv"]
# ///

import requests
from dotenv import load_dotenv
load_dotenv()

# Your hook logic here
```

**Configuration not loading** requires checking the `/hooks` command interface, validating JSON syntax with `jq . .claude/settings.json`, and ensuring settings files are in the correct locations. Remember that changes require session restart or explicit reload.

**Debugging hook execution** benefits from comprehensive logging:

```python
#!/usr/bin/env python3
import json
import sys
import logging
from pathlib import Path

# Set up logging
log_dir = Path.home() / '.claude' / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    filename=log_dir / 'hooks.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log all input data
data = json.load(sys.stdin)
logging.info(f"Hook triggered: {data.get('hook_event_name')}")
logging.debug(f"Full payload: {json.dumps(data, indent=2)}")

# Your hook logic here
try:
    # Process the hook
    pass
except Exception as e:
    logging.error(f"Hook failed: {str(e)}", exc_info=True)
    sys.exit(1)
```

## Best practices for production deployment

Successful hook deployment in team environments requires thoughtful organization and clear documentation. Structure your hooks directory for maintainability:

```
.claude/
├── settings.json              # Team-shared configuration
├── settings.local.json        # Personal overrides
├── hooks/
│   ├── README.md             # Hook documentation
│   ├── pre_tool_use.py       # Security validation
│   ├── post_tool_use.py      # Quality checks
│   ├── notification.py       # Alert system
│   ├── session_start.py      # Context loading
│   └── lib/                  # Shared utilities
│       ├── security.py
│       └── formatters.py
├── commands/                  # Custom slash commands
└── context.md                # Project context
```

Document each hook's purpose, expected behavior, and any dependencies. Include examples of when hooks will trigger and what actions they'll take. This documentation becomes invaluable when onboarding new team members or debugging issues.

Start with simple, well-tested hooks and gradually increase complexity. Begin with a basic formatter, add security validations, then implement notifications and advanced workflows. This incremental approach reduces the risk of breaking your development flow while building powerful automation.

## Working example: Auto-commit hook

Here's a proven auto-commit hook configuration that automatically commits changes after file edits:

**Configuration in `.claude/settings.local.json`:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'set -euo pipefail; git add -A; if [ -z \"$(git diff --cached)\" ]; then exit 0; fi; ts=$(date +%F_%T); msg=\"chore(write): auto-commit $ts\"; files=$(git diff --cached --name-status | sed \"s/^/  • /\"); git commit -m \"$msg\" -m \"$files\";'",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

This hook:
- Triggers after any file edit operation
- Automatically stages all changes with `git add -A`
- Checks if there are actual changes to commit
- Creates a timestamped commit message
- Lists changed files in the commit body
- Uses proper error handling with `set -euo pipefail`

## Common pitfalls and solutions

**Hook location mistakes**: Place hook configurations in `.claude/settings.json` or `.claude/settings.local.json`, NOT in `.claude/hooks/` directory. The hooks directory is for hook scripts, not configurations.

**Matcher pattern issues**: 
- Use `"Edit|Write|MultiEdit"` to catch all file modifications
- Empty string `""` matches all tools (not `"*"` which doesn't work)
- Tool names are case-sensitive

**Template variable problems**: Template variables like `{{tool.name}}` don't get replaced in current versions. Use environment variables instead:
- `$CLAUDE_FILE_PATHS` - Files being edited
- `$CLAUDE_PROJECT_DIR` - Project root directory
- `$CLAUDE_TOOL_NAME` - Name of the tool being used

**Session restart requirements**: After modifying hook configurations, you may need to restart your Claude Code session for changes to take effect. The system captures hook snapshots at startup.

**Exit code confusion**: 
- Exit code 0 = success (hook output shown to user)
- Exit code 2 = blocking error (stderr sent to Claude as feedback)
- Other codes = non-blocking error (stderr shown to user)

**Testing hooks**: Create a simple echo hook first to verify the system is working:
```json
{
  "type": "command",
  "command": "echo 'Hook triggered!' >> /tmp/claude-hook-test.log",
  "timeout": 10
}
```

## The transformative power of deterministic automation

Claude Code hooks transform probabilistic AI assistance into deterministic development automation. By encoding your team's best practices, security requirements, and workflow preferences as hooks, you create an AI assistant that not only understands your codebase but reliably follows your exact specifications every time.
