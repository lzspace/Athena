#!/usr/bin/env bash
# Category: Issue Sync
# Updates existing GitHub Issues with rich metadata from TODO.md.
# - Adds description, @due(...) date, and @prio(...) priority tag
# - Replaces the "unknown" label with proper category
# - Use after editing existing TODOs with more info

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"
TODO_FILE="TODO.md"

valid_labels=("future" "ai" "planning" "productivity" "work" "personal" "science" "unknown" "priority_high" "priority_medium" "priority_low")

is_valid_label() {
  for label in "${valid_labels[@]}"; do
    [[ "$1" == "$label" ]] && return 0
  done
  return 1
}

normalize_label() {
  echo "$1" \
    | sed -E 's/#+\s+//' \
    | sed -E 's/[^a-zA-Z0-9]+/_/g' \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/^_+|_+$//g'
}

current_label="unknown"
collect_description=false
description=""
title=""
due=""
priority=""

while IFS= read -r line || [[ -n $line ]]; do
  if [[ "$line" == \#\#* ]]; then
    raw=$(normalize_label "$line")
    is_valid_label "$raw" && current_label="$raw" || current_label="unknown"
    continue
  fi

  # New task
  if [[ "$line" == "- [ ]"* ]]; then
    # Submit the last one if any
    if [[ -n "$title" ]]; then
      issue_number=$(gh issue list -R "$REPO" --state open --json title,number | jq -r \
        --arg TITLE "$title" '.[] | select(.title == $TITLE) | .number')

      if [[ -n "$issue_number" ]]; then
        echo "🔄 Updating #$issue_number '$title'"
        full_body="$description"
        [[ -n "$due" ]] && full_body+="\n\n📆 Due: $due"
        [[ -n "$priority" ]] && full_body+="\n🔺 Priority: $priority"

        gh issue edit "$issue_number" -R "$REPO" \
          --body "$full_body" \
          --add-label "$current_label" \
          --remove-label "unknown"

        # Add priority label
        if [[ -n "$priority" ]]; then
          gh issue edit "$issue_number" -R "$REPO" --add-label "priority_${priority,,}"
        fi
      else
        echo "⚠️  Issue not found: $title"
      fi
    fi

    # Start a new one
    title=$(echo "$line" | sed -E 's/- \[ \] //')
    description=""
    due=""
    priority=""
    collect_description=true
    continue
  fi

  # Metadata tags in the following lines
  if $collect_description; then
    if [[ "$line" =~ @due\(([0-9]{4}-[0-9]{2}-[0-9]{2})\) ]]; then
      due="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ @prio\((high|medium|low)\) ]]; then
      priority="${BASH_REMATCH[1]}"
    elif [[ "$line" =~ ^- \[ \] ]]; then
      collect_description=false
    else
      description+="$line"$'\n'
    fi
  fi

done < "$TODO_FILE"

echo "✅ Enhanced issue update complete!"
