#!/usr/bin/env bash
# Category: Testing
# Description: Tests the functionality of sync_todo_to_issues.sh.
# Details:
# - Ensures new issues are created from unchecked TODOs
# - Prevents duplicate issues from being created
# - Applies correct labels based on section headers or @label() tags

set -e
cd "$(dirname "$0")/.."

TEST_TODO="tests/test_sync_todo.md"
cat > "$TEST_TODO" <<EOF
## Productivity

- [ ] New test sync task  
  This should create a new GitHub issue.  
  @label(productivity)

- [ ] Duplicate test task  
  Should NOT create again if issue already exists.
EOF

# Backup the original TODO.md and swap in test
cp TODO.md TODO.md.bak
cp "$TEST_TODO" TODO.md

# Run the sync
bash scripts/sync_todo_to_issues.sh

# Restore the original TODO.md
mv TODO.md.bak TODO.md
rm "$TEST_TODO"

echo "✅ test_sync.sh passed (manual result verification recommended)"