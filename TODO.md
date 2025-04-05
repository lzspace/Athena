## 🌟 Productivity

- [x] Enable bi-directional sync between TODO.md and GitHub Issues  
  Let's implement a two-way sync where checked TODOs close GitHub issues.  
  @due(2025-04-15) @prio(high) @milestone(Personal :: Tasks)

- [x] Implement milestones  
  Use GitHub milestones to plan short- and long-term project goals.  
  @due(2025-05-01) @prio(medium) @milestone(Personal :: Tasks)

- [ ] Sync from GitHub Issues to TODO.md  
  Allow syncing manually created issues back into the TODO list.  
  @prio(medium) @label(productivity) @milestone(Personal :: Tasks)

- [x] Automatically close GitHub Issues when TODOs are checked off  
  Ensures tasks are marked complete everywhere.  
  @prio(high) @label(productivity) @milestone(Personal :: Tasks)

- [x] Highlight outdated TODOs when related issues are closed  
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

- [ ] Create `assistant_core/` directory for the primary assistant logic  
  Provides a dedicated space for code handling user messages, routing, etc.  
  @prio(high) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Implement an NLP-based intent matching system  
  Use a lightweight model or rule-based approach to detect user intent (e.g., “schedule an appointment”).  
  @prio(high) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Integrate appointment logic into NLP pipeline  
  When a user asks “Schedule a meeting tomorrow at 9,” call `create_appointment`.  
  @prio(medium) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Build out AI conflict resolution flow  
  If a conflict arises, the assistant prompts: “That time conflicts with X. Reschedule or override?”  
  @prio(medium) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Conduct end-to-end tests for assistant + appointment scheduling  
  e.g., parse “Please schedule dentist on Monday at 10am” → create appointment → confirm success.  
  @prio(medium) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Enhance user feedback and conversation style  
  Format success/error messages in a friendly, conversational manner (via text or TTS).  
  @prio(low) @label(assistant) @milestone(Assistant :: LLM Integration)

- [ ] Future extension: add voice interface integration  
  Send STT transcripts through the same NLP pipeline.  
  @prio(low) @label(assistant) @milestone(Assistant :: Voice)

## 🏷 Personal: Appointments

- [x] Set up a local SQLite database for appointments  
  Initialize a new `appointments.db` (or reuse an existing DB).  
  @prio(high) @label(personal) @milestone(Personal :: Appointments)

- [x] Create an `appointments` table with columns (id, title, start_time, end_time, location, description, created_at, updated_at)  
  Store essential appointment info in SQLite for quick retrieval.  
  @prio(high) @label(personal) @milestone(Personal :: Appointments)

- [x] Implement a Python module `appointments.py` with basic CRUD  
  `create_appointment`, `list_appointments`, `get_appointment_by_id`, `update_appointment`, `delete_appointment`.  
  @prio(medium) @label(personal) @milestone(Personal :: Appointments)

- [x] Write tests for appointment CRUD  
  Use either Python’s `unittest` or `pytest` for verifying DB reads/writes.  
  @prio(medium) @label(personal) @milestone(Personal :: Appointments)

- [ ] Explore AI-based scheduling approach  
  Integrate dateparser, conflict detection, or GPT-based suggestions to find free times.  
  @prio(low) @label(personal) @milestone(Personal :: Appointments)

- [ ] Optional: Plan future calendar sync (Google, Android)  
  For direct or partial synchronization with external calendars.  
  @prio(low) @label(personal) @milestone(Personal :: Appointments)
