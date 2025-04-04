## 🎯 Productivity

- [ ] Enable bi-directional sync between TODO.md and GitHub Issues  
  Let's implement a two-way sync where checked TODOs close GitHub issues.  
  @due(2025-04-15) @prio(high)

- [ ] Implement milestones  
  Use GitHub milestones to plan short- and long-term project goals.  
  @due(2025-05-01) @prio(medium)

  ## 🧪 Testing & Validation

- [ ] Create a test script to validate script headers (shebang, category, description)
  Ensures consistency and supports cheatsheet generation.  
  @prio(high) @due(2025-04-10)

- [ ] Set up a Git pre-commit hook to run header validation before every commit  
  Blocks commits if required fields are missing.  
  @prio(high)

- [ ] Create a dedicated `tests/` directory for all validation scripts  
  Helps keep the codebase organized and scalable.  
  @prio(medium)

- [ ] Add a "test" label to all test-related GitHub issues for better filtering  
  Visual separation of validation and utility tasks.  
  @prio(low)

- [ ] Add a future `test_all.sh` or `Makefile` to run all validation and sync tests together  
  Supports automation and continuous validation.  
  @prio(medium)