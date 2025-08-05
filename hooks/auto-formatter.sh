#!/bin/bash
# Auto-formatter Hook for Claude Code
# ===================================
#
# This PostToolUse hook automatically formats Python files using ruff.
# It runs both ruff check (linting) and ruff format (formatting).
#
# Usage:
# Add to .claude/settings.json under PostToolUse hooks:
# {
#   "matcher": "Edit|Write|MultiEdit",
#   "hooks": [{
#     "type": "command",
#     "command": "bash hooks/auto-formatter.sh",
#     "timeout": 30
#   }]
# }

# Exit on any error
set -euo pipefail

# Check if CLAUDE_FILE_PATHS is set
if [ -z "${CLAUDE_FILE_PATHS:-}" ]; then
    echo "No files to format"
    exit 0
fi

# Process each file
for file in $CLAUDE_FILE_PATHS; do
    # Only process Python files
    if [[ "$file" == *.py ]]; then
        echo "Processing Python file: $file"
        
        # Run ruff check with auto-fix
        echo "Running ruff check --fix on $file"
        ruff check --fix "$file" || true
        
        # Run ruff format
        echo "Running ruff format on $file"
        ruff format "$file" || true
        
        echo "Completed formatting for $file"
    fi
done

echo "Auto-formatting complete"