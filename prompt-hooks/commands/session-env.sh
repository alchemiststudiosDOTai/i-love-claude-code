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
