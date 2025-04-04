#!/usr/bin/env bash

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"
TODO_FILE="TODO.md"

valid_labels=("future" "ai" "planning" "productivity" "work" "personal" "science" "unknown")

echo "🔄 Syncing TODO.md with GitHub Issues..."

current_label="unknown"

# Helper to validate labels
is_valid_label() {
  for label in "${valid_labels[@]}"; do
    [[ "$1" == "$label" ]] && return 0
  done
  return 1
}

while IFS= read -r line || [[ -n $line ]]; do
  # Skip empty lines
  [[ -z "$line" ]] && continue

  # Section headers → labels
  if [[ "$line" == \#\#* ]]; then
    raw=$(echo "$line" | sed -E 's/#+\s+//; s/[🌌🌍🧠📅🎯💡🚀]//g; s/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]')
    if is_valid_label "$raw"; then
      current_label="$raw"
    else
      current_label="unknown"
    fi
    continue
  fi

  # Unchecked task
    if [[ "$line" == "- [ ]"* ]]; then
    title=$(echo "$line" | sed -E 's/- \[ \] //')

    # Check for existing issue
    if gh issue list -R "$REPO" --limit 100 | grep -q "$title"; then
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