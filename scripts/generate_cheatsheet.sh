#!/usr/bin/env bash
# Creates GitHub Issues from unchecked TODOs in TODO.md
# Avoids duplicates and labels based on section headers
# Run this after adding new TODOs

cd "$(dirname "$0")/.."

OUT_FILE="CHEATSHEET.md"
SCRIPTS_DIR="scripts"

echo "# 🧠 Athena Assistant Script Cheatsheet" > "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "This file is generated from script headers in \`$SCRIPTS_DIR/\`." >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

for script in "$SCRIPTS_DIR"/*.sh; do
  [[ -f "$script" ]] || continue

  title=$(basename "$script")
  echo "## 🔧 \`$title\`" >> "$OUT_FILE"

  # Read doc comments (first consecutive lines starting with #)
  description_block=""
  while IFS= read -r line; do
    if [[ "$line" =~ ^\# ]]; then
      stripped=$(echo "$line" | sed 's/^#\s*//')
      description_block+="$stripped"$'\n'
    else
      break
    fi
  done < "$script"

  echo "$description_block" >> "$OUT_FILE"

  echo '```bash' >> "$OUT_FILE"
  echo "bash $script" >> "$OUT_FILE"
  echo '```' >> "$OUT_FILE"
  echo "" >> "$OUT_FILE"
done

echo "✅ Generated $OUT_FILE"