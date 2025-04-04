# Athena Makefile

# Run all validation tests
check:
	bash tests/test_headers.sh

# Push changes to GitHub
push:
	bash scripts/git_push.sh

# Sync TODO.md with GitHub Issues and update metadata
sync:
	bash scripts/sync_todo_to_issues.sh
	bash scripts/update_issues.sh

# Generate script documentation
cheatsheet:
	python3 scripts/generate_cheatsheet.py

# Run all essential actions
all: check sync cheatsheet push

# Used by pre-commit: validate headers, generate cheatsheet, and run all tests
precommit:
	cd $(dir $(realpath $(lastword $(MAKEFILE_LIST)))) && make check && make cheatsheet && make test

# Run all available tests
test:
	bash tests/test_all.sh
	bash tests/test_update_metadata.sh
	bash tests/test_close_issues.sh

# Update GitHub issues if TODOs are completed
autosync:
	bash scripts/update_issues.sh --close-done
