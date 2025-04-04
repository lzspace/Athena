#!/usr/bin/env bash
# Category: Testing
# Description: Tests metadata sync (description, @prio, @label, @due) using update_issues.sh.
# Details:
# - Creates a temporary TODO with metadata
# - Verifies correct label assignment and body update in GitHub (manual check)

set -e
cd "$(dirname "$0")/.."

TEST_TODO="tests/test_todo_metadata.md"
cat > "$TEST_TODO" <<EOF
## Test

- [ ] __TEST: Metadata sync  
  This issue should be updated with correct metadata.  
  @prio(high) @due(2025-05-01) @label(test)
EOF

cp TODO.md TODO.md.bak
cp "$TEST_TODO" TODO.md

bash scripts/update_issues.sh

mv TODO.md.bak TODO.md
rm "$TEST_TODO"

echo "✅ test_update_metadata.sh passed (manual result verification recommended)"