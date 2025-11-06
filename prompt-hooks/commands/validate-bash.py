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
        (r'\bgrep\b(?!\s+--)', 'Use Grep tool instead of grep command'),
        (r'\brg\b', 'Use Grep tool instead of ripgrep command'),
        (r'\bfind\b', 'Use Glob tool instead of find command'),
        (r'\$\w+(?!["\'])', 'Unquoted variable expansion detected'),
        (r'rm\s+-rf\s+/(?!tmp|var)', 'Dangerous rm -rf on root directory'),
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
            # Check for shebang or existing header comments
            has_header = content.startswith(("#!", "# File:", '"""', "'''"))
            if not has_header:
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
