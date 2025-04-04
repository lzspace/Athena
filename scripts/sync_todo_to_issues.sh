#!/bin/bash

cd "$(dirname "$0")/.."

REPO="luisziegler/Athena"
TODO_FILE="TODO.md"

echo "🔄 Syncing TODO.md with GitHub Issues..."

# Store current section (e.g. ## Future Ideas)
current_label="general"

while IFS= read -r line; do
  # Detect headers and convert them to labels (e.g., ## 🌌 Future Ideas → future)
  if [[ $line == ##* ]]; then
    current_label=$(echo "$line" | sed -E 's/#+\s+//; s/[🌌🌍🧠📅🎯💡]//g; s/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]')
    continue
  fi

  # Match unchecked tasks
  if [[ $line =~ ^- \[ \] ]]; then
    title=$(echo "$line" | sed -E 's/- \[ \] //')

    # Check if the issue already exists
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
