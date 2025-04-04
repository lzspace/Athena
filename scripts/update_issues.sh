#!/usr/bin/env bash
# Category: Issue Sync
# Description: Updates GitHub Issues with metadata and correct labels from TODO.md.
# Details:
# - Adds description, @due(...) dates, @prio(...) and @label(...) overrides
# - Supports @milestone(...) to assign issues to GitHub milestones
# - Replaces 'unknown' label with parsed section or explicit tag
# - Closes GitHub issues if matching TODO is marked as completed and --close-done is passed

cd "$(dirname "$0")/.."

REPO="lzspace/Athena"
TODO_FILE="TODO.md"
CLOSE_DONE=false

[[ "$1" == "--close-done" ]] && CLOSE_DONE=true

valid_labels=("future" "ai" "planning" "productivity" "work" "personal" "science" "test" "assistant" "unknown" "priority_high" "priority_medium" "priority_low")

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
title=""
description=""
due=""
priority=""
custom_label=""
milestone=""
done=false
collect_description=false

while IFS= read -r line || [[ -n "$line" ]]; do
  [[ -z "$line" ]] && continue

  if [[ "$line" == "##"* ]]; then
    raw=$(normalize_label "$line")
    is_valid_label "$raw" && current_label="$raw" || current_label="unknown"
    continue
  fi

  if echo "$line" | grep -qE "^- \[x\]"; then
    done=true
    line="- [ ]${line:5}"
  else
    done=false
  fi

  if [[ "$line" == "- [ ]"* ]]; then
    if [[ -n "$title" ]]; then
      issue_number=$(gh issue list -R "$REPO" --state open --json title,number | jq -r --arg TITLE "$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[[:space:]]//g')" '.[] | select(.title | ascii_downcase | gsub("[[:space:]]"; "") == $TITLE) | .number')
      if [[ -n "$issue_number" ]]; then
        if $done && $CLOSE_DONE; then
          echo "✅ Closing issue #$issue_number for completed task"
          gh issue close "$issue_number" -R "$REPO"
        else
          echo "🔄 Updating #$issue_number '$title'"
          full_body="$description"
          [[ -n "$due" ]] && full_body+=$'\n\n📆 Due: '$due
          [[ -n "$priority" ]] && full_body+=$'\n🔹 Priority: '$priority

          final_label="$current_label"
          if [[ -n "$custom_label" ]] && is_valid_label "$custom_label"; then
            final_label="$custom_label"
          fi

          gh issue edit "$issue_number" -R "$REPO" \
            --body "$full_body" \
            --add-label "$final_label" \
            --remove-label "unknown"

          if [[ -n "$priority" ]]; then
            label="priority_${priority}"
            label=$(echo "$label" | tr '[:upper:]' '[:lower:]')
            gh issue edit "$issue_number" -R "$REPO" --add-label "$label"
          fi

          if [[ -n "$milestone" ]]; then
            milestone_number=$(gh api repos/$REPO/milestones --jq ".[] | select(.title == \"$milestone\") | .number")
            if [[ -n "$milestone_number" ]]; then
              gh issue edit "$issue_number" -R "$REPO" --milestone "$milestone_number"
            fi
          fi
        fi
      else
        echo "⚠️  Issue not found: $title"
      fi
    fi

    title=$(echo "$line" | sed -E 's/- \[ \] //')
    description=""
    due=""
    priority=""
    custom_label=""
    milestone=""
    collect_description=true
    continue
  fi

  if $collect_description; then
    if [[ "$line" == *"@due("* ]]; then
      due=$(echo "$line" | sed -nE 's/.*@due\(([^)]+)\).*/\1/p')
    elif [[ "$line" == *"@prio("* ]]; then
      priority=$(echo "$line" | sed -nE 's/.*@prio\(([^)]+)\).*/\1/p')
    elif [[ "$line" == *"@label("* ]]; then
      custom_label=$(echo "$line" | sed -nE 's/.*@label\(([^)]+)\).*/\1/p')
    elif [[ "$line" == *"@milestone("* ]]; then
      milestone=$(echo "$line" | sed -nE 's/.*@milestone\(([^)]+)\).*/\1/p')
    elif [[ "$line" == "- [ ]"* ]]; then
      collect_description=false
    else
      description+="$line"$'\n'
    fi
  fi

done < "$TODO_FILE"

echo "✅ Issue label updates complete!"
