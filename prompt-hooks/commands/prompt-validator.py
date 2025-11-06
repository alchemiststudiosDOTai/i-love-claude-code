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
    r'(?i)(password|passwd|pwd)\s*[:=]\s*(["\'][^"\']{8,}["\']|[^\s]{8,})',
    r'sk-[a-zA-Z0-9]{32,}',  # OpenAI-style keys
    r'ghp_[a-zA-Z0-9]{36}',  # GitHub tokens (exactly 36 chars)
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
