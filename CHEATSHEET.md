# 🧠 Athena Assistant Script Cheatsheet

This file is generated from script headers in `scripts/`.

## 🔧 `create_labels.sh`
!/usr/bin/env bash

```bash
bash scripts/create_labels.sh
```

## 🔧 `create_priority_labels.sh`
!/usr/bin/env bash
 Category: Project Admin
 Creates priority labels: priority_high, priority_medium, priority_low.
 - Used for visual task triage
 - Labels are applied automatically when @prio(...) is found

```bash
bash scripts/create_priority_labels.sh
```

## 🔧 `generate_cheatsheet.sh`
!/usr/bin/env bash
 Creates GitHub Issues from unchecked TODOs in TODO.md
 Avoids duplicates and labels based on section headers
 Run this after adding new TODOs

```bash
bash scripts/generate_cheatsheet.sh
```

## 🔧 `git_push.sh`
!/bin/bash
 Category: Utilities
 A simple wrapper script for fast Git commits and pushes.
 - Prompts for a commit message (or uses "Update" by default)
 - Adds and pushes all modified files

```bash
bash scripts/git_push.sh
```

## 🔧 `sync_todo_to_issues.sh`
!/usr/bin/env bash

```bash
bash scripts/sync_todo_to_issues.sh
```

## 🔧 `update_issue_labels.sh`
!/usr/bin/env bash
 Category: Issue Sync
 Updates existing GitHub Issues with rich metadata from TODO.md.
 - Adds description, @due(...) date, and @prio(...) priority tag
 - Replaces the "unknown" label with proper category
 - Use after editing existing TODOs with more info

```bash
bash scripts/update_issue_labels.sh
```

