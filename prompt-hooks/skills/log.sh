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
