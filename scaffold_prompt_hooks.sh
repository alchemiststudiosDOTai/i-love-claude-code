#!/usr/bin/env bash
set -euo pipefail

# scaffold_prompt_hooks.sh
# Creates a complete prompt-hooks scaffold with conventional bash commands + prompt-based hooks
# For: alchemiststudiosDOTai/i-love-claude-code

echo "=== Scaffolding Claude Code Prompt Hooks ==="

# Create directory structure
mkdir -p prompt-hooks/{commands,subagents,skills,examples/plugin}
mkdir -p .claude/hooks

echo "✓ Created directory structure"

# ============================================================
# SKILLS (reusable utilities)
# ============================================================

cat <<'EOF' > prompt-hooks/skills/log.sh
#!/usr/bin/env bash
# Structured logger for hooks

log_json() {
    local level="$1"
    local message="$2"
    local meta="${3:-{}}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    printf '{"timestamp":"%s","level":"%s","message":"%s","meta":%s}\n' \
        "$timestamp" "$level" "$message" "$meta"
}

# Usage: log_json "info" "Hook executed" '{"hook":"PreToolUse"}'
EOF

chmod +x prompt-hooks/skills/log.sh

echo "✓ Created skills/log.sh"

# ============================================================
# SUBAGENTS (helper scripts invoked by commands)
# ============================================================

cat <<'EOF' > prompt-hooks/subagents/file_rules.sh
#!/usr/bin/env bash
# Check file rules (e.g., license header requirement)
# Returns non-zero if rules violated

file_path="${1:-}"

if [[ -z "$file_path" ]]; then
    echo "Usage: file_rules.sh <file_path>" >&2
    exit 1
fi

# Check if file exists
if [[ ! -f "$file_path" ]]; then
    echo "File not found: $file_path" >&2
    exit 1
fi

# Check for license header in source files
if [[ "$file_path" =~ \.(py|js|ts|sh)$ ]]; then
    if ! head -n 5 "$file_path" | grep -qi "license\|copyright\|SPDX"; then
        echo "Missing license header in: $file_path" >&2
        exit 2
    fi
fi

echo "File rules passed for: $file_path"
exit 0
EOF

chmod +x prompt-hooks/subagents/file_rules.sh

echo "✓ Created subagents/file_rules.sh"

# ============================================================
# COMMANDS - PreToolUse (Write|Edit|Bash)
# ============================================================

cat <<'EOF' > prompt-hooks/commands/validate-bash.py
#!/usr/bin/env python3
"""
PreToolUse hook: Validates bash commands for unsafe patterns.
Returns JSON with permissionDecision: deny|allow|ask
"""

import sys
import json
import re

def validate_bash(command: str) -> dict:
    """Check for unsafe bash patterns"""
    unsafe_patterns = [
        (r'\bgrep\b', 'Use Grep tool instead of grep command'),
        (r'\brg\b', 'Use Grep tool instead of ripgrep command'),
        (r'\bfind\b', 'Use Glob tool instead of find command'),
        (r'\$\w+\b(?!["\'])', 'Unquoted variable expansion - ensure variables are quoted'),
        (r'rm\s+-rf\s+/', 'Dangerous rm -rf on root paths'),
    ]

    for pattern, reason in unsafe_patterns:
        if re.search(pattern, command):
            return {
                "permissionDecision": "deny",
                "reason": reason,
                "hookSpecificOutput": {
                    "pattern": pattern,
                    "command": command[:100]
                }
            }

    return {"permissionDecision": "allow"}

def main():
    # Read hook context from stdin
    try:
        context = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"permissionDecision": "allow"}))
        return

    tool_input = context.get("toolInput", {})
    tool_name = context.get("toolName", "")

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        result = validate_bash(command)
    elif tool_name in ["Write", "Edit"]:
        # Example: add file header for Write operations
        file_path = tool_input.get("file_path", "")
        if tool_name == "Write" and file_path.endswith(('.py', '.sh')):
            content = tool_input.get("content", "")
            if not content.startswith("#"):
                # Provide updatedInput to add header
                result = {
                    "permissionDecision": "allow",
                    "updatedInput": {
                        "content": f"# File: {file_path}\n{content}"
                    },
                    "hookSpecificOutput": {
                        "message": "Added file header"
                    }
                }
            else:
                result = {"permissionDecision": "allow"}
        else:
            result = {"permissionDecision": "allow"}
    else:
        result = {"permissionDecision": "allow"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
EOF

chmod +x prompt-hooks/commands/validate-bash.py

echo "✓ Created commands/validate-bash.py (PreToolUse)"

# ============================================================
# COMMANDS - PostToolUse (Write|Edit)
# ============================================================

cat <<'EOF' > prompt-hooks/commands/post-write-context.py
#!/usr/bin/env python3
"""
PostToolUse hook: Validates written files and adds context.
Returns decision: block|continue with hookSpecificOutput.additionalContext
"""

import sys
import json
import subprocess
import os

def check_file_rules(file_path: str) -> tuple:
    """Run subagent to check file rules"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    subagent = os.path.join(script_dir, "..", "subagents", "file_rules.sh")

    if not os.path.exists(subagent):
        return (True, "Subagent not found")

    try:
        result = subprocess.run(
            [subagent, file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return (True, result.stdout.strip())
        else:
            return (False, result.stderr.strip())
    except Exception as e:
        return (True, f"Check failed: {e}")

def main():
    try:
        context = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({"decision": "continue"}))
        return

    tool_input = context.get("toolInput", {})
    tool_name = context.get("toolName", "")
    file_path = tool_input.get("file_path", "")

    if tool_name in ["Write", "Edit"] and file_path:
        # Check file rules via subagent
        passed, message = check_file_rules(file_path)

        if not passed:
            result = {
                "decision": "block",
                "reason": f"File validation failed: {message}",
                "hookSpecificOutput": {
                    "validationError": message,
                    "filePath": file_path
                }
            }
        else:
            result = {
                "decision": "continue",
                "hookSpecificOutput": {
                    "additionalContext": f"✓ File validated: {file_path}\n{message}"
                }
            }
    else:
        result = {"decision": "continue"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
EOF

chmod +x prompt-hooks/commands/post-write-context.py

echo "✓ Created commands/post-write-context.py (PostToolUse)"

# ============================================================
# COMMANDS - UserPromptSubmit
# ============================================================

cat <<'EOF' > prompt-hooks/commands/prompt-validator.py
#!/usr/bin/env python3
"""
UserPromptSubmit hook: Validates prompts for potential secrets.
Special case: prints context to stdout (not JSON) on success.
Shows JSON control approach in comments.
"""

import sys
import json
import re
from datetime import datetime

SECRET_PATTERNS = [
    r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}',
    r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{8,}',
    r'sk-[a-zA-Z0-9]{32,}',  # OpenAI-style keys
    r'ghp_[a-zA-Z0-9]{36,}',  # GitHub tokens
    r'(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*',
]

def check_secrets(prompt: str) -> tuple:
    """Check for potential secrets in prompt"""
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, prompt):
            return (True, f"Potential secret detected: pattern {pattern[:30]}...")
    return (False, "")

def main():
    try:
        context = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Fallback: allow with timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] Prompt validated")
        return

    prompt = context.get("prompt", "")
    has_secret, reason = check_secrets(prompt)

    if has_secret:
        # JSON control approach (commented for reference):
        # result = {
        #     "decision": "block",
        #     "reason": reason,
        #     "systemMessage": "Your prompt contains potential secrets. Please remove them."
        # }
        # print(json.dumps(result, indent=2))

        # For demo: actually use JSON
        result = {
            "decision": "block",
            "reason": reason,
            "systemMessage": "🔒 Prompt contains potential secrets. Please review and remove sensitive data."
        }
        print(json.dumps(result, indent=2))
    else:
        # Success case: print context to stdout (special case for UserPromptSubmit)
        # This demonstrates non-JSON output that gets shown to user
        timestamp = datetime.utcnow().isoformat() + "Z"
        print(f"[{timestamp}] ✓ Prompt validated - no secrets detected")

        # Alternative JSON approach (commented):
        # result = {
        #     "decision": "continue",
        #     "hookSpecificOutput": {
        #         "additionalContext": f"[{timestamp}] Prompt validated"
        #     }
        # }
        # print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
EOF

chmod +x prompt-hooks/commands/prompt-validator.py

echo "✓ Created commands/prompt-validator.py (UserPromptSubmit)"

# ============================================================
# COMMANDS - SessionStart
# ============================================================

cat <<'EOF' > prompt-hooks/commands/session-env.sh
#!/usr/bin/env bash
# SessionStart hook: Initialize session environment
# Demonstrates nvm use and env persistence via CLAUDE_ENV_FILE

set -euo pipefail

MATCHER="${1:-unknown}"
CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE:-/tmp/claude_session_env.json}"

# Source log utility
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../skills/log.sh" 2>/dev/null || true

log_message() {
    if command -v log_json &>/dev/null; then
        log_json "info" "$1" "{\"matcher\":\"$MATCHER\"}"
    else
        echo "[INFO] $1"
    fi
}

# Handle different session start types
case "$MATCHER" in
    startup)
        log_message "New session startup"
        # Initialize environment file
        echo '{"sessionStart":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'","nodeVersion":""}' > "$CLAUDE_ENV_FILE"

        # Try to use nvm if available
        if command -v nvm &>/dev/null; then
            nvm use 20 &>/dev/null || true
            NODE_VERSION=$(node --version 2>/dev/null || echo "unknown")
            # Update env file with node version
            TMP_FILE=$(mktemp)
            jq --arg nv "$NODE_VERSION" '.nodeVersion = $nv' "$CLAUDE_ENV_FILE" > "$TMP_FILE"
            mv "$TMP_FILE" "$CLAUDE_ENV_FILE"
            log_message "Using Node.js $NODE_VERSION"
        fi
        ;;
    resume)
        log_message "Resuming previous session"
        if [[ -f "$CLAUDE_ENV_FILE" ]]; then
            PREV_NODE=$(jq -r '.nodeVersion // "unknown"' "$CLAUDE_ENV_FILE")
            log_message "Previous Node.js version: $PREV_NODE"
        fi
        ;;
    clear|compact)
        log_message "Session cleared/compacted"
        ;;
    *)
        log_message "Unknown session event: $MATCHER"
        ;;
esac

# Output context (shown to Claude)
echo ""
echo "=== Session Environment ==="
echo "Event: $MATCHER"
echo "Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
[[ -f "$CLAUDE_ENV_FILE" ]] && echo "Env state: $(cat "$CLAUDE_ENV_FILE")"
echo "==========================="
EOF

chmod +x prompt-hooks/commands/session-env.sh

echo "✓ Created commands/session-env.sh (SessionStart)"

# ============================================================
# PROMPT-BASED HOOKS - Stop & SubagentStop
# ============================================================

cat <<'EOF' > .claude/hooks/stop-guard.prompt.txt
You are a safety guard for Claude Code operations. Your task is to decide whether to approve or block a stop/cancel request.

Context provided:
- reason: Why the stop was requested
- conversationLength: Number of messages in conversation
- lastToolUse: Information about the last tool that was used
- currentTask: Description of what Claude is currently doing

Response schema (you MUST respond with valid JSON only):
{
  "decision": "approve" | "block",
  "reason": "Explanation for your decision",
  "continue": false,
  "stopReason": "user_request" | "safety" | "error",
  "systemMessage": "Optional message to show the user"
}

Decision criteria:
- APPROVE if: User explicitly requested stop, no critical operation in progress, safe stopping point
- BLOCK if: Critical file operation mid-write, destructive command executing, data loss risk

Consider the safety of stopping at this moment. If blocking, explain what needs to complete first.

User stop request context:
$ARGUMENTS

Analyze the context and respond with JSON only.
EOF

echo "✓ Created .claude/hooks/stop-guard.prompt.txt (prompt-based hook)"

# ============================================================
# EXAMPLES - Plugin hooks
# ============================================================

cat <<'EOF' > prompt-hooks/examples/plugin/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "${CLAUDE_PLUGIN_ROOT}/format-file.sh $FILE_PATH",
        "timeout": 30,
        "description": "Auto-format written files using plugin formatter",
        "enabled": true
      }
    ]
  },
  "metadata": {
    "name": "auto-formatter-plugin",
    "version": "1.0.0",
    "description": "Example plugin demonstrating PostToolUse with ${CLAUDE_PLUGIN_ROOT}"
  }
}
EOF

cat <<'EOF' > prompt-hooks/examples/plugin/format-file.sh
#!/usr/bin/env bash
# Example formatter plugin script

FILE_PATH="${1:-}"

if [[ -z "$FILE_PATH" ]]; then
    echo "Usage: format-file.sh <file_path>" >&2
    exit 1
fi

# Simulate formatting
echo "Formatting $FILE_PATH..."

case "$FILE_PATH" in
    *.py)
        # Would run: black "$FILE_PATH" 2>/dev/null || true
        echo "✓ Python file formatted"
        ;;
    *.js|*.ts)
        # Would run: prettier --write "$FILE_PATH" 2>/dev/null || true
        echo "✓ JavaScript/TypeScript file formatted"
        ;;
    *)
        echo "No formatter for this file type"
        ;;
esac

exit 0
EOF

chmod +x prompt-hooks/examples/plugin/format-file.sh

echo "✓ Created examples/plugin/ (PostToolUse auto-format)"

# ============================================================
# EXAMPLES - Minimal runnable samples
# ============================================================

cat <<'EOF' > prompt-hooks/examples/minimal-pretooluse.sh
#!/usr/bin/env bash
# Minimal PreToolUse example - always allow with log

echo '{"permissionDecision":"allow","hookSpecificOutput":{"message":"Hook executed"}}'
EOF

chmod +x prompt-hooks/examples/minimal-pretooluse.sh

cat <<'EOF' > prompt-hooks/examples/minimal-posttooluse.sh
#!/usr/bin/env bash
# Minimal PostToolUse example - continue with context

echo '{"decision":"continue","hookSpecificOutput":{"additionalContext":"Operation completed successfully"}}'
EOF

chmod +x prompt-hooks/examples/minimal-posttooluse.sh

echo "✓ Created examples/minimal-*.sh"

# ============================================================
# .claude/settings.json - Complete hook configuration
# NOTE: This scaffold script is the source of truth for settings.json.
# The standalone .claude/settings.json file should not be edited separately.
# ============================================================

cat <<'EOF' > .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/validate-bash.py",
        "timeout": 5,
        "description": "Validate bash commands for unsafe patterns",
        "enabled": true
      },
      {
        "matcher": "Write|Edit",
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/validate-bash.py",
        "timeout": 5,
        "description": "Add file headers to new files",
        "enabled": true
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/post-write-context.py",
        "timeout": 10,
        "description": "Validate written files and check license headers",
        "enabled": true
      }
    ],
    "UserPromptSubmit": [
      {
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/prompt-validator.py",
        "timeout": 3,
        "description": "Check prompts for potential secrets",
        "enabled": true
      }
    ],
    "Stop": [
      {
        "type": "prompt",
        "prompt": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-guard.prompt.txt",
        "timeout": 10,
        "description": "LLM-based safety guard for stop requests",
        "enabled": true,
        "arguments": {
          "reason": "$STOP_REASON",
          "conversationLength": "$CONVERSATION_LENGTH",
          "lastToolUse": "$LAST_TOOL",
          "currentTask": "$CURRENT_TASK"
        }
      }
    ],
    "SubagentStop": [
      {
        "type": "prompt",
        "prompt": "$CLAUDE_PROJECT_DIR/.claude/hooks/stop-guard.prompt.txt",
        "timeout": 8,
        "description": "LLM-based guard for subagent cancellation",
        "enabled": true,
        "arguments": {
          "reason": "$STOP_REASON",
          "subagentId": "$SUBAGENT_ID"
        }
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/session-env.sh $MATCHER",
        "timeout": 15,
        "description": "Initialize session environment and persist state",
        "enabled": true
      }
    ],
    "PreCompact": [
      {
        "matcher": "manual|auto",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-style.sh",
        "timeout": 5,
        "description": "Check code style before compacting context",
        "enabled": true
      }
    ],
    "MCP": [
      {
        "matcher": "mcp__.*__write.*",
        "command": "$CLAUDE_PROJECT_DIR/prompt-hooks/commands/post-write-context.py",
        "timeout": 10,
        "description": "Validate MCP write operations",
        "enabled": false
      }
    ]
  },
  "hookDefaults": {
    "timeout": 10,
    "enabled": true
  },
  "metadata": {
    "version": "1.0.0",
    "description": "Complete prompt-hooks scaffold with bash and prompt-based hooks",
    "repository": "alchemiststudiosDOTai/i-love-claude-code"
  }
}
EOF

echo "✓ Created .claude/settings.json"

# ============================================================
# .claude/hooks - Additional project-local hook scripts
# ============================================================

cat <<'EOF' > .claude/hooks/check-style.sh
#!/usr/bin/env bash
# PreCompact hook example: check code style before compacting

MATCHER="${1:-manual}"

echo "=== Style Check (PreCompact) ==="
echo "Trigger: $MATCHER"

# Simple check: look for common style issues
ISSUES=0

if command -v shellcheck &>/dev/null; then
    if find . -name "*.sh" -type f -print0 | xargs -0 shellcheck -S warning 2>/dev/null; then
        echo "✓ Shell scripts pass basic checks"
    else
        echo "⚠ Shell script warnings found"
        ((ISSUES++))
    fi
fi

if [[ $ISSUES -gt 0 ]]; then
    echo "Found $ISSUES style issue(s) - consider fixing before compact"
else
    echo "✓ No style issues detected"
fi

exit 0
EOF

chmod +x .claude/hooks/check-style.sh

echo "✓ Created .claude/hooks/check-style.sh"

# ============================================================
# README.md - Documentation
# ============================================================

cat <<'EOF' > prompt-hooks/README.md
# Claude Code Prompt Hooks Scaffold

Complete implementation of Claude Code hooks combining conventional bash commands with prompt-based LLM hooks.

## Structure

```
prompt-hooks/
├── commands/          # Hook command scripts (bash & Python)
├── subagents/         # Helper scripts invoked by commands
├── skills/            # Reusable utilities/library code
├── examples/          # Minimal runnable samples
└── README.md

.claude/
├── settings.json      # Hook configuration and wiring
└── hooks/             # Project-local hook scripts
```

## Installed Hooks

### PreToolUse (Write|Edit|Bash)
- **validate-bash.py**: Blocks unsafe patterns (plain grep, unquoted vars, dangerous rm)
- Returns JSON with `permissionDecision`: "deny" | "allow" | "ask"
- Can provide `updatedInput` to modify tool parameters (e.g., add file headers)

### PostToolUse (Write|Edit)
- **post-write-context.py**: Validates files after writing
- Blocks operations if file rules fail (e.g., missing license header)
- Returns `decision`: "block" | "continue" with `additionalContext`
- Invokes `subagents/file_rules.sh` for validation logic

### UserPromptSubmit
- **prompt-validator.py**: Checks prompts for potential secrets
- Blocks prompts containing API keys, passwords, tokens
- On success: prints timestamp context to stdout (special case)
- Demonstrates both stdout and JSON control approaches

### Stop & SubagentStop (Prompt-based)
- **stop-guard.prompt.txt**: LLM-powered safety guard
- Decides whether to approve or block stop requests
- Response schema: `{decision, reason, continue, stopReason, systemMessage}`
- Uses `$ARGUMENTS` for context passing

### SessionStart (startup|resume|clear|compact)
- **session-env.sh**: Initialize session environment
- Persists state via `CLAUDE_ENV_FILE`
- Demonstrates `nvm use 20` with version tracking
- Provides environment context to Claude

### PreCompact (manual|auto)
- **check-style.sh**: Validates code style before context compaction
- Non-blocking (informational only)
- Runs shellcheck if available

### MCP Example
- Matcher: `mcp__.*__write.*`
- Validates MCP write operations using post-write-context.py

## Quick Start

```bash
# Run the scaffold script
bash scaffold_prompt_hooks.sh

# Hooks are automatically wired in .claude/settings.json
# They'll execute based on matchers when Claude Code runs

# Test a hook manually
echo '{"toolName":"Bash","toolInput":{"command":"grep foo bar"}}' | \
  ./prompt-hooks/commands/validate-bash.py

# Expected output: {"permissionDecision": "deny", ...}
```

## Debugging

### Enable debug mode
```bash
claude --debug
```

### Four progress messages in transcript mode

1. **Hook triggered**: `Running PreToolUse hook: validate-bash.py`
2. **Command executed**: `Executing: /path/to/validate-bash.py`
3. **Status**: `✓ Hook succeeded` or `✗ Hook failed (exit 1)`
4. **Output**: JSON response or error messages

### Common issues

- **Permission denied**: Ensure scripts are executable (`chmod +x`)
- **Timeout**: Adjust timeout in settings.json (default: 10s)
- **Python errors**: Check `python3 -m py_compile commands/*.py`
- **Path issues**: Use `$CLAUDE_PROJECT_DIR` for project-relative paths

## Safety Notes

⚠️ **Important**:
- Hooks can block operations - test carefully before enabling
- PreToolUse denial prevents tool execution entirely
- PostToolUse blocks show errors to user but don't prevent writes (file already written)
- Stop hooks can prevent user from canceling operations
- Always include timeouts to prevent hanging
- Prompt-based hooks send context to LLM - avoid secrets in $ARGUMENTS

## JSON Control Schemas

### PreToolUse Response
```json
{
  "permissionDecision": "allow" | "deny" | "ask",
  "reason": "Why decision was made",
  "updatedInput": {
    "parameter": "modified value"
  },
  "hookSpecificOutput": {}
}
```

### PostToolUse Response
```json
{
  "decision": "continue" | "block",
  "reason": "Why operation should continue/block",
  "hookSpecificOutput": {
    "additionalContext": "Context added to conversation"
  }
}
```

### UserPromptSubmit Response
```json
{
  "decision": "continue" | "block",
  "reason": "Why prompt should continue/block",
  "systemMessage": "Message shown to user if blocked"
}
```

### Stop/SubagentStop Response (Prompt-based)
```json
{
  "decision": "approve" | "block",
  "reason": "Why stop should be approved/blocked",
  "continue": false,
  "stopReason": "user_request" | "safety" | "error",
  "systemMessage": "Message shown to user"
}
```

## Environment Variables

- `$CLAUDE_PROJECT_DIR`: Project root directory
- `$CLAUDE_ENV_FILE`: Session state persistence file
- `$CLAUDE_PLUGIN_ROOT`: Plugin installation directory
- `$ARGUMENTS`: Context passed to prompt-based hooks
- `$MATCHER`: Hook matcher pattern (for SessionStart, etc.)
- `$STOP_REASON`, `$CONVERSATION_LENGTH`, etc.: Hook-specific context

## Examples

See `examples/` for minimal runnable samples:
- `minimal-pretooluse.sh`: Always-allow PreToolUse hook
- `minimal-posttooluse.sh`: Continue with context
- `plugin/`: Auto-formatter plugin using `${CLAUDE_PLUGIN_ROOT}`

## Contributing

When adding new hooks:
1. Place command scripts in `commands/`
2. Extract complex logic to `subagents/`
3. Share utilities via `skills/`
4. Add configuration to `.claude/settings.json`
5. Test with `--debug` flag
6. Document in this README

## License

Part of i-love-claude-code documentation repository.
EOF

echo "✓ Created prompt-hooks/README.md"

# ============================================================
# Self-test function
# ============================================================

self_test() {
    echo ""
    echo "=== Self-Test ==="
    echo ""

    echo "1. Directory structure:"
    if command -v tree &>/dev/null; then
        tree prompt-hooks -L 2
    else
        find prompt-hooks -type f -o -type d | sort | sed 's|^|  |'
    fi
    echo ""

    echo "2. Hook configuration (first 40 lines):"
    if command -v jq &>/dev/null; then
        jq '.hooks' .claude/settings.json | head -n 40
    else
        grep -A 40 '"hooks"' .claude/settings.json
    fi
    echo ""

    echo "3. Python syntax check:"
    PYTHON_OK=true
    for pyfile in prompt-hooks/commands/*.py; do
        if [[ -f "$pyfile" ]]; then
            if python3 -m py_compile "$pyfile" 2>/dev/null; then
                echo "  ✓ $pyfile"
            else
                echo "  ✗ $pyfile - syntax error"
                PYTHON_OK=false
            fi
        fi
    done

    echo ""
    echo "4. Executable permissions:"
    find prompt-hooks -type f \( -name "*.sh" -o -name "*.py" \) -perm /111 | sed 's|^|  ✓ |'

    echo ""
    if $PYTHON_OK; then
        echo "=== All checks passed ==="
    else
        echo "=== Some checks failed - review above ==="
    fi
}

# Run self-test
self_test

echo ""
echo "=== Scaffold Complete ==="
echo ""
echo "Next steps:"
echo "1. Review .claude/settings.json and adjust matchers/timeouts"
echo "2. Test hooks with: claude --debug"
echo "3. Customize prompt-hooks/commands/ for your needs"
echo "4. Add project-specific rules to subagents/"
echo ""
echo "Documentation: prompt-hooks/README.md"
echo ""
