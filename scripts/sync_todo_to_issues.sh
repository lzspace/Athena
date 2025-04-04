#!/usr/bin/env bash
# Category: Issue Sync
# Syncs unchecked tasks from TODO.md to GitHub Issues.
# - Avoids duplicate issues by exact title match
# - Assigns a section-based label (e.g. "productivity", "ai")
# - Use this after adding new tasks to your TODO list

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"
TODO_FILE="TODO.md"

# Define valid labels
valid_labels=("future" "ai" "planning" "productivity" "work" "personal" "science" "unknown")

echo "🔄 Syncing TODO.md with GitHub Issues..."

current_label="unknown"

# Helper: Check if a label is valid
is_valid_label() {
  for label in "${valid_labels[@]}"; do
    [[ "$1" == "$label" ]] && return 0
  done
  return 1
}

# Get existing issue titles to avoid duplicates
existing_issues=$(gh issue list -R "$REPO" --state open --limit 100 --json title | jq -r '.[].title')

while IFS= read -r line || [[ -n $line ]]; do
  # Skip empty lines
  if [[ -z "$line" ]]; then
    continue
  fi

  # Section headers → labels
  if [[ "$line" == \#\#* ]]; then
 raw=$(echo "$line" \
  | sed -E 's/#+\s+//' \
  | sed -E 's/[^a-zA-Z0-9]+/_/g' \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/^_+|_+$//g')

# Add this debug line if you like
# echo "→ Raw section label: $raw"

if is_valid_label "$raw"; then
  current_label="$raw"
else
  current_label="unknown"
fi
echo "→ Section: '$line' → Label: '$current_label'"
  # Match unchecked tasks
  if [[ "$line" == "- [ ]"* ]]; then
    title=$(echo "$line" | sed -E 's/- \[ \] //')

    # Check if title already exists exactly
    if echo "$existing_issues" | grep -Fxq "$title"; then
      echo "⚠️  Issue already exists: $title"
    else
      echo "➕ Creating issue: $title [label: $current_label]"
      gh issue create -R "$REPO" \
        --title "$title" \
        --body "Imported from TODO.md (section: $current_label)" \
        --label "$current_label"
    fi
  fi
done < "$TODO_FILE"

echo "✅ Sync complete!"