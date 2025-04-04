#!/usr/bin/env bash

cd "$(dirname "$0")/.."

OUT_FILE="CHEATSHEET.md"
SCRIPTS_DIR="scripts"

echo "# 🧠 Athena Assistant Script Cheatsheet" > "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "This file is dynamically generated from script headers in \`$SCRIPTS_DIR/\`." >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

# Collect categories and script info
declare -A grouped

for script in "$SCRIPTS_DIR"/*.sh; do
  [[ -f "$script" ]] || continue

  title=$(basename "$script")
  category="Uncategorized"
  command="bash $script"
  description=""

  # Read script header
  while IFS= read -r line; do
    [[ -z "$line" ]] && break
    if [[ "$line" == \#\ Category:* ]]; then
      category=$(echo "$line" | sed 's/# Category: //')
    elif [[ "$line" == \#* ]]; then
      description+="${line#\# }"$'\n'
    else
      break
    fi
  done < "$script"

  grouped["$category"]+=$'\n'"## 🔧 \`$title\`"$'\n\n'"```bash"$'\n'"$command"$'\n'"```"$'\n\n'"**Category:** $category"$'\n'"$description"$'\n'"---"$'\n'
done

# Print categories in preferred order
categories=("Issue Sync" "Project Admin" "Utilities" "DevOps" "Assistant Core" "Uncategorized")

for cat in "${categories[@]}"; do
  [[ -n "${grouped[$cat]}" ]] && echo "## 🔷 $cat" >> "$OUT_FILE" && echo "${grouped[$cat]}" >> "$OUT_FILE"
done

echo "✅ Cheatsheet generated: $OUT_FILE"
