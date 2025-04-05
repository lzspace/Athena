#!/usr/bin/env bash
# Category: Git Hooks
# Description: Pre-commit hook for validating commit messages and running tests.
# Details:
# - Validates commit messages to ensure they follow a specific format.
# - Runs tests to ensure code quality and functionality.
# - Aborts the commit if any checks fail.

# Fail on any error
set -e


echo "🔒 Running pre-commit checks..."

bash tests/test_headers.sh
RESULT=$?

if [ $RESULT -ne 0 ]; then
  echo "❌ Commit aborted: header validation failed."
  exit 1
fi

echo "✅ Header check passed."


# Set Python path for correct imports
export PYTHONPATH=$(pwd)

# Run tests in all subdirectories under tests/
echo "🔍 Running tests..."
pytest tests/ --disable-warnings

echo "✅ All tests passed."