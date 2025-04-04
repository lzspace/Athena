#!/usr/bin/env bash
# Category: Testing
# Description: Tests auto-closing of GitHub issues when TODOs are completed.
# Details:
# - Injects a checked task into TODO
# - Runs update_issues.sh with --close-done
# - Confirms the issue is closed (manual check required)

set -e
cd "$(dirname "$0")/.."

TEST_TODO="tests/test_todo_closing.md"
cat > "$TEST_TODO" <<EOF
## Test

- [x] __TEST: Close issue if done  
  This task should trigger issue closure.  
  @label(test)
EOF

cp TODO.md TODO.md.bak
cp "$TEST_TODO" TODO.md

bash scripts/update_issues.sh --close-done

mv TODO.md.bak TODO.md
rm "$TEST_TODO"

echo "✅ test_close_issues.sh passed (manual check of GitHub issue status suggested)"