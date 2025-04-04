#!/usr/bin/env bash
# Category: Issue Sync
# Description: Creates GitHub Issues from TODO.md entries.
# Details:
# - Avoids duplicates by checking existing issue titles
# - Applies labels based on section headers or @label() tag

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"
TODO_FILE="TODO.md"

valid_labels=("future" "ai" "planning" "productivity" "work" "personal" "science" "test" "assistant" "unknown")

is_valid_label() {
  for label in "${valid_labels[@]}"; do
    [[ "$1" == "$label" ]] && return 0
  done
  return 1
}

echo "🔄 Syncing TODO.md with GitHub Issues..."

current_label="unknown"
existing_issues=$(gh issue list -R "$REPO" --state open --limit 100 --json title | jq -r '.[].title')

while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue

  if [[ "$line" == \#\#* ]]; then
    raw=$(echo "$line" \
      | sed -E 's/#+\s+//' \
      | sed -E 's/[^a-zA-Z0-9]+/_/g' \
      | tr '[:upper:]' '[:lower:]' \
      | sed -E 's/^_+|_+$//g')
    if is_valid_label "$raw"; then
      current_label="$raw"
    else
      current_label="unknown"
    fi
    continue
  fi

  if [[ "$line" == "- [ ]"* ]]; then
    title=$(echo "$line" | sed -E 's/- \[ \] //')
    custom_label=""
    next_line=1
    continue
  fi

  # Metadata parsing for label override
  if [[ "$line" == *"@label("* ]]; then
    custom_label=$(echo "$line" | sed -nE 's/.*@label\(([^)]+)\).*/\1/p')
    if is_valid_label "$custom_label"; then
      current_label="$custom_label"
    fi
  fi

  if [[ -n "$title" && "$line" == "" ]]; then
    if echo "$existing_issues" | grep -Fxq "$title"; then
      echo "⚠️  Issue already exists: $title"
    else
      echo "➕ Creating issue: $title [label: $current_label]"
      gh issue create -R "$REPO" \
        --title "$title" \
        --body "Imported from TODO.md (section or tag: $current_label)" \
        --label "$current_label"
    fi
    title=""
  fi

done < "$TODO_FILE"

echo "✅ Sync complete!"
