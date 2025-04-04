#!/usr/bin/env bash
# Category: Project Admin
# Creates priority labels: priority_high, priority_medium, priority_low.
# - Used for visual task triage
# - Labels are applied automatically when @prio(...) is found

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"

echo "🏷️ Creating priority labels..."

# Label definitions
priorities=(
  "priority_high|High priority|ff4d4d"
  "priority_medium|Medium priority|ffc107"
  "priority_low|Low priority|28a745"
)

for entry in "${priorities[@]}"; do
  IFS="|" read -r label desc color <<< "$entry"

  if gh label list -R "$REPO" | grep -q "^$label"; then
    echo "✅ Label already exists: $label"
  else
    echo "➕ Creating label: $label"
    gh label create "$label" \
      --repo "$REPO" \
      --description "$desc" \
      --color "$color"
  fi
done

echo "🎉 Priority labels created or verified!"
