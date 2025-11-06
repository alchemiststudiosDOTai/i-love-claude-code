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
