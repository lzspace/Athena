#!/bin/bash

cd "$(dirname "$0")/.."

echo "📦 Staging changes..."
git add .

echo "📝 Commit message (default: 'Update'):"
read msg
msg=${msg:-"Update"}

git commit -m "$msg"
git push origin main

echo "✅ Push complete!"

906D-3F01