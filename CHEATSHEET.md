# 🧠 Athena Assistant Script Cheatsheet

This file is dynamically generated from script metadata.

## 🔷 Issue Sync

### 🔧 `sync_todo_to_issues.sh`

```bash
bash scripts/sync_todo_to_issues.sh
```

**Category:** Issue Sync  
**Description:** Creates GitHub Issues from TODO.md entries.

- Avoids duplicates by checking existing issue titles
- Applies labels based on section headers or @label() tag

### 🔧 `update_issues.sh`

```bash
bash scripts/update_issues.sh
```

**Category:** Issue Sync  
**Description:** Updates GitHub Issues with metadata and correct labels from TODO.md.

- Adds description, @due(...) dates, @prio(...) and @label(...) overrides
- Replaces 'unknown' label with parsed section or explicit tag

---

## 🔷 Project Admin

### 🔧 `create_labels.sh`

```bash
bash scripts/create_labels.sh
```

**Category:** Project Admin  
**Description:** Creates your core category labels on GitHub.

- Skips labels that already exist
- Used for section-based labeling of issues

### 🔧 `create_priority_labels.sh`

```bash
bash scripts/create_priority_labels.sh
```

**Category:** Project Admin  
**Description:** Creates priority labels (high, medium, low) on GitHub.

- Supports label-based priority tagging via @prio(...) in TODO.md

---

## 🔷 Utilities

### 🔧 `generate_cheatsheet.py`

```bash
python3 scripts/generate_cheatsheet.py
```

**Category:** Utilities  
**Description:** Dynamically generates CHEATSHEET.md from script metadata.

- Reads category, description, and details blocks
- Groups output by category

### 🔧 `git_push.sh`

```bash
bash scripts/git_push.sh
```

**Category:** Utilities  
**Description:** Simple wrapper script for Git add, commit and push.

- Prompts for commit message or uses 'Update'
- Stashes, commits, and pushes all changes

### 🔧 `test_headers.sh`

```bash
bash scripts/test_headers.sh
```

**Category:** Utilities  
**Description:** Validates that all Athena scripts have required documentation headers.

- Checks for shebang, Category, and Description fields
- Flags missing headers with line numbers

---
