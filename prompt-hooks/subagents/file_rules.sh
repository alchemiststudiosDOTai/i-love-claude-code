#!/usr/bin/env bash
# Check file rules (e.g., license header requirement)
# Returns non-zero if rules violated

file_path="${1:-}"

if [[ -z "$file_path" ]]; then
    echo "Usage: file_rules.sh <file_path>" >&2
    exit 3
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
