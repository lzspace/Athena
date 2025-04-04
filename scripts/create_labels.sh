#!/usr/bin/env bash
# Category: Project Admin
# Description: Creates GitHub labels for category organization.


cd "$(dirname "$0")/.."

REPO="lzspace/Athena"

echo "🏷️ Creating GitHub labels..."

# Label name → description pairs
valid_labels=(
  "future" "ai" "planning" "productivity" "work" "personal" "science" "test"
  "testing_validation" "assistant_core_planning" "unknown"
  "priority_high" "priority_medium" "priority_low"
)
label_descriptions=(
  "AI-related tasks"
  "Planned or conceptual ideas"
  "Scheduling, time, and logistics"
  "Scientific knowledge or logic"
  "Work-related topics"
  "Personal goals, reflections, notes"
  "Task and system optimization"
  "Uncategorized or later-review tasks"
)

for i in "${!label_names[@]}"; do
  label="${label_names[$i]}"
  desc="${label_descriptions[$i]}"

  if gh label list -R "$REPO" | grep -q "^$label"; then
    echo "✅ Label already exists: $label"
  else
    echo "➕ Creating label: $label"
    gh label create "$label" \
      --repo "$REPO" \
      --description "$desc" \
      --color "cccccc"
  fi
done

echo "🎉 All labels created or verified!"