#!/usr/bin/env bash
# Category: Testing
# Description: Runs all available test scripts for Athena.
# Details:
# - Executes each test script under tests/ with logging
# - Used to validate sync/update workflows and header checks

set -e
cd "$(dirname "$0")"

echo "🔍 Running all Athena tests..."

for test_script in test_*.sh; do
  [[ "$test_script" == "test_all.sh" ]] && continue
  echo "\n▶ Running: $test_script"
  bash "$test_script" | tee -a test_logs.log
  echo "✅ $test_script completed"
done

echo "🎉 All tests passed."
