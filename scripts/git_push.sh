#!/usr/bin/env bash
# Category: Utilities
# Description: Fast Git commit and push script. With pre-commit checks.
# A simple wrapper script for fast Git commits and pushes.
# - Prompts for a commit message (or uses "Update" by default)
# - Adds and pushes all modified files

cd "$(dirname "$0")/.."

echo "📦 Staging changes..."
git add .

echo "📝 Commit message (default: 'Update'):"
read msg
msg=${msg:-"Update"}

git commit -m "$msg"
git push origin main

echo "✅ Push complete!"

