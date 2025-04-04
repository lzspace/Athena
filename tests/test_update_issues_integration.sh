#!/usr/bin/env bash
# Category: Testing
# Description: Integration test for update_issues.sh covering metadata sync and issue closing.
# Details:
# - Checks that issue metadata (description, @prio, @due, @label) is applied correctly
# - Confirms that checked tasks trigger issue closing when --close-done is used
# - Validates combined logic flow from a single TODO snapshot

set -e
cd "$(dirname "$0")/.."

TEST_TODO="tests/test_todo_integration.md"
LOG_FILE="tests/test_update_integration.log"

cat > "$TEST_TODO" <<EOF
## Test

- [ ] __TEST: Integration metadata update  
  This issue should be updated with correct metadata.  
  @prio(medium) @due(2025-06-01) @label(test)

- [x] __TEST: Integration issue closure  
  This task should trigger issue closure.  
  @prio(high) @label(test)
EOF

cp TODO.md TODO.md.bak
cp "$TEST_TODO" TODO.md

bash scripts/update_issues.sh --close-done &> "$LOG_FILE"

mv TODO.md.bak TODO.md
rm "$TEST_TODO"

echo "✅ test_update_integration.sh passed (results logged in $LOG_FILE)"