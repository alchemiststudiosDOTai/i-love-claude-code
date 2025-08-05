#!/usr/bin/env python3
"""
Security Validation Hook for Claude Code
========================================

This PreToolUse hook validates file operations and commands to prevent
potentially dangerous actions. It blocks operations on sensitive files
and dangerous shell commands.

Usage:
Add to .claude/settings.json under PreToolUse hooks:
{
  "matcher": "Edit|Write|MultiEdit|Bash",
  "hooks": [{
    "type": "command",
    "command": "python3 hooks/security-validator.py",
    "timeout": 30
  }]
}
"""

import json
import sys
import re
import os
from pathlib import Path

# Load the hook payload from stdin
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    print("Error: Invalid JSON input", file=sys.stderr)
    sys.exit(1)

tool_name = data.get('tool_name', '')
tool_input = data.get('tool_input', {})

# Define sensitive file patterns
SENSITIVE_PATTERNS = [
    r'\.env(\.|$)',           # .env files
    r'\.git/',                 # Git internals
    r'id_rsa',                 # SSH private keys
    r'id_ed25519',            # SSH private keys
    r'\.pem$',                # Certificate files
    r'\.key$',                # Key files
    r'/etc/',                 # System config
    r'~/.ssh/',               # SSH directory
    r'\.htpasswd',            # Password files
    r'secrets?\.',            # Files with 'secret' in name
    r'password',              # Password files
    r'token\.json',           # Token files
    r'\.aws/',                # AWS credentials
    r'\.kube/',               # Kubernetes configs
]

# Define dangerous command patterns
DANGEROUS_COMMANDS = [
    r'rm\s+.*-[rf]',          # rm -rf variants
    r'sudo\s+rm',             # sudo rm commands
    r'chmod\s+777',           # Dangerous permissions
    r'chmod\s+.*-R.*777',     # Recursive dangerous perms
    r'>\s*/etc/',             # Writing to system dirs
    r'>\s*/usr/',             # Writing to system dirs
    r'curl.*\|.*bash',        # Pipe curl to bash
    r'wget.*\|.*sh',          # Pipe wget to shell
    r'mkfs',                  # Filesystem formatting
    r'dd\s+if=.*of=/dev/',    # Direct disk writes
    r':(){.*:\|:&}',          # Fork bomb
    r'nc\s+-l',               # Netcat listeners
]

def check_path_security(file_path):
    """Check if a file path is safe to access"""
    # Normalize the path
    path = Path(file_path).resolve()
    path_str = str(path)
    
    # Check for path traversal
    if '..' in file_path:
        return False, "Path traversal detected"
    
    # Check against sensitive patterns
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, path_str, re.IGNORECASE):
            return False, f"Access denied: matches sensitive pattern '{pattern}'"
    
    # Check if trying to write outside project directory
    project_dir = os.getenv('CLAUDE_PROJECT_DIR', os.getcwd())
    if not path_str.startswith(project_dir):
        return False, "Access denied: outside project directory"
    
    return True, None

def check_command_security(command):
    """Check if a shell command is safe to execute"""
    # Check against dangerous patterns
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, f"Command blocked: matches dangerous pattern"
    
    # Check for attempts to modify sensitive directories
    sensitive_dirs = ['/etc', '/usr', '/boot', '/sys', '/proc']
    for dir in sensitive_dirs:
        if dir in command and ('>' in command or 'mv' in command or 'cp' in command):
            return False, f"Command blocked: attempts to modify {dir}"
    
    return True, None

# Main validation logic
if tool_name in ['Edit', 'Write', 'MultiEdit']:
    file_path = tool_input.get('file_path', '')
    if file_path:
        is_safe, reason = check_path_security(file_path)
        if not is_safe:
            response = {
                "decision": "block",
                "reason": reason
            }
            print(json.dumps(response))
            sys.exit(0)

elif tool_name == 'Bash':
    command = tool_input.get('command', '')
    if command:
        is_safe, reason = check_command_security(command)
        if not is_safe:
            response = {
                "decision": "block", 
                "reason": reason
            }
            print(json.dumps(response))
            sys.exit(0)

# If we get here, the operation is allowed
sys.exit(0)