#!/usr/bin/env bash
# Category: Utilities
# Description: Validates that all Athena scripts have required documentation headers.
# Details:
# - Checks for shebang, Category, and Description fields
# - Flags missing headers with line numbers
# - Run manually or hook into pre-commit system

cd "$(dirname "$0")/.."

fail_count=0

echo "🔍 Checking script headers in scripts/..."

for script in scripts/*.sh; do
  [[ -f "$script" ]] || continue
  echo "🧪 $script"

  # Check for shebang
  if ! grep -q '^#!/usr/bin/env bash' "$script"; then
    echo "  ❌ Missing or incorrect shebang"
    ((fail_count++))
  fi

  # Check for Category
  if ! grep -q '^# Category: ' "$script"; then
    echo "  ❌ Missing '# Category:' header"
    ((fail_count++))
  fi

  # Check for Description
  if ! grep -q '^# Description: ' "$script"; then
    echo "  ❌ Missing '# Description:' header"
    ((fail_count++))
  fi

done

if [[ $fail_count -eq 0 ]]; then
  echo "✅ All scripts have valid headers!"
else
  echo "❗ $fail_count issues found. Please fix headers above."
  exit 1
fi
