## 🌟 Productivity

- [ ] Enable bi-directional sync between TODO.md and GitHub Issues  
  Let's implement a two-way sync where checked TODOs close GitHub issues.  
  @due(2025-04-15) @prio(high) @milestone(Personal :: Tasks)

- [ ] Implement milestones  
  Use GitHub milestones to plan short- and long-term project goals.  
  @due(2025-05-01) @prio(medium) @milestone(Personal :: Tasks)

- [ ] Sync from GitHub Issues to TODO.md  
  Allow syncing manually created issues back into the TODO list.  
  @prio(medium) @label(productivity) @milestone(Personal :: Tasks)

- [x] Automatically close GitHub Issues when TODOs are checked off  
  Ensures tasks are marked complete everywhere.  
  @prio(high) @label(productivity) @milestone(Personal :: Tasks)

- [ ] Highlight outdated TODOs when related issues are closed  
  Adds warnings or indicators in TODO.md for closed issues.  
  @prio(medium) @label(productivity) @milestone(Personal :: Tasks)

## 🪪 Testing & Validation

- [x] Create a test script to validate script headers (shebang, category, description)  
  Ensures consistency and supports cheatsheet generation.  
  @prio(high) @due(2025-04-10) @label(test) @milestone(Testing :: Coverage)

- [x] Set up a Git pre-commit hook to run header validation before every commit  
  Blocks commits if required fields are missing.  
  @prio(high) @label(test) @milestone(Testing :: Infrastructure)

- [x] Create a dedicated `tests/` directory for all validation scripts  
  Helps keep the codebase organized and scalable.  
  @prio(medium) @label(test) @milestone(Testing :: Infrastructure)

- [x] Add a "test" label to all test-related GitHub issues for better filtering  
  Visual separation of validation and utility tasks.  
  @prio(low) @label(test) @milestone(Testing :: Coverage)

- [x] Add a future `test_all.sh` or `Makefile` to run all validation and sync tests together  
  Supports automation and continuous validation.  
  @prio(medium) @label(test) @milestone(Testing :: Infrastructure)

- [x] Validate TODO.md structure and metadata  
  Check for missing labels, invalid @prio tags, or formatting problems.  
  @prio(medium) @label(test) @milestone(Testing :: Coverage)

- [x] Auto-insert script header templates into new scripts  
  Helps enforce documentation standards automatically.  
  @prio(low) @label(test) @milestone(Testing :: Infrastructure)

- [x] Create `test_sync.sh` to validate sync_todo_to_issues.sh  
  Covers issue creation, duplication prevention, and label assignment.  
  @prio(high) @label(test) @milestone(Testing :: Coverage)

- [x] Create `test_update_issues.sh` to validate update_issues.sh  
  Tests label/metadata sync and issue closing on completed TODOs.  
  @prio(high) @label(test) @milestone(Testing :: Coverage)

- [x] Document all test scripts in CHEATSHEET.md  
  Ensure test files are listed with category, description, and usage.  
  @prio(medium) @label(test) @milestone(Testing :: Coverage)

- [x] Create integration test for update_issues.sh  
  Full flow test for metadata update + issue closing  
  @prio(high) @label(test) @milestone(Testing :: Coverage)

## 🚀 Assistant Core Planning

- [ ] Create `assistant_core/` directory for future LLM and UI logic  
  Prepares the system to host inference, tools, routing, etc.  
  @prio(medium) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Add a voice interface stub for future audio I/O  
  Set up placeholder for audio command support.  
  @prio(low) @label(assistant) @milestone(Assistant :: Voice)

- [ ] Build a smart task categorizer (LLM-assisted)  
  Automatically suggests label and priority from task text.  
  @prio(medium) @label(assistant) @milestone(Assistant :: LLM Integration)
