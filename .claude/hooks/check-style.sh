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
