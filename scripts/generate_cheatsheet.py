#!/usr/bin/env python3
# Category: Utilities
# Description: Dynamically generates CHEATSHEET.md from script metadata.
# Details:
# - Scans known scripts and groups them by category
# - Outputs full descriptions, usage, and command examples

from pathlib import Path
from collections import defaultdict

scripts_info = [
    {
        "file": "sync_todo_to_issues.sh",
        "category": "Issue Sync",
        "description": "Creates GitHub Issues from TODO.md entries.",
        "details": [
            "Avoids duplicates by checking existing issue titles",
            "Applies labels based on section headers or @label() tag"
        ]
    },
    {
        "file": "update_issues.sh",
        "category": "Issue Sync",
        "description": "Updates GitHub Issues with metadata and correct labels from TODO.md.",
        "details": [
            "Adds description, @due(...) dates, @prio(...) and @label(...) overrides",
            "Replaces 'unknown' label with parsed section or explicit tag"
        ]
    },
    {
        "file": "test_headers.sh",
        "category": "Utilities",
        "description": "Validates that all Athena scripts have required documentation headers.",
        "details": [
            "Checks for shebang, Category, and Description fields",
            "Flags missing headers with line numbers"
        ]
    },
    {
        "file": "generate_cheatsheet.py",
        "category": "Utilities",
        "description": "Dynamically generates CHEATSHEET.md from script metadata.",
        "details": [
            "Reads category, description, and details blocks",
            "Groups output by category"
        ]
    },
    {
        "file": "create_labels.sh",
        "category": "Project Admin",
        "description": "Creates your core category labels on GitHub.",
        "details": [
            "Skips labels that already exist",
            "Used for section-based labeling of issues"
        ]
    },
    {
        "file": "create_priority_labels.sh",
        "category": "Project Admin",
        "description": "Creates priority labels (high, medium, low) on GitHub.",
        "details": [
            "Supports label-based priority tagging via @prio(...) in TODO.md"
        ]
    },
    {
        "file": "git_push.sh",
        "category": "Utilities",
        "description": "Simple wrapper script for Git add, commit and push.",
        "details": [
            "Prompts for commit message or uses 'Update'",
            "Stashes, commits, and pushes all changes"
        ]
    }
]

# Generate markdown
lines = ["# 🧠 Athena Assistant Script Cheatsheet", "", "This file is dynamically generated from script metadata.", ""]

by_category = defaultdict(list)
for info in scripts_info:
    by_category[info["category"]].append(info)

for category in sorted(by_category):
    lines.append(f"## 🔷 {category}\n")
    for script in sorted(by_category[category], key=lambda s: s["file"]):
        lines.append(f"### 🔧 `{script['file']}`\n")
        lines.append("```bash")
        lines.append(f"bash scripts/{script['file']}" if script['file'].endswith('.sh') else f"python3 scripts/{script['file']}")
        lines.append("```")
        lines.append("")
        lines.append(f"**Category:** {script['category']}  ")
        lines.append(f"**Description:** {script['description']}")
        lines.append("")
        for detail in script.get("details", []):
            lines.append(f"- {detail}")
        lines.append("")
    lines.append("---\n")

# Save to file
Path("CHEATSHEET.md").write_text("\n".join(lines))
print("✅ CHEATSHEET.md has been generated!")