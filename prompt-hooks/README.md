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
