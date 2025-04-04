#!/usr/bin/env bash
# Category: Project Admin
# Description: Creates GitHub milestones in the repo for organizing issues.
# Details:
# - Helps group issues by domain (Personal, Assistant, Testing)
# - Milestones are referenced using @milestone(...) in TODO.md or scripts

set -e
REPO="lzspace/Athena"

milestones=(
  "Personal :: Tasks"
  "Personal :: Notes"
  "Personal :: Appointments"
  "Assistant :: Sync"
  "Assistant :: LLM Integration"
  "Assistant :: Voice"
  "Testing :: Coverage"
  "Testing :: Infrastructure"
)

for milestone in "${milestones[@]}"; do
  echo "📌 Creating milestone: $milestone"
  gh api repos/$REPO/milestones \
    -f title="$milestone" \
    -f state="open" > /dev/null || echo "⚠️  Could not create: $milestone"
done

echo "✅ All milestones created (or already existed)."