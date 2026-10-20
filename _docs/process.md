# Development Process

## Overview

This project follows a spec-driven, multi-agent engineering process.

## Roles

- **PM**: Grooms a task before implementation using `_docs/team/pm.md`.
- **Engineer**: Implements one groomed task following `_docs/team/software-engineer.md`.
- **QA**: Verifies implementation against acceptance criteria using `_docs/team/qa-engineer.md`.

## Orchestrator Lifecycle

1. Pick the next open issue from the backlog.
2. PM grooms the issue into `_docs/task-template.md` format.
3. Engineer implements the task and adds tests.
4. QA runs verification tests and checks acceptance criteria.
5. If QA outputs `FAIL`, loop back to step 3 with failure details.
6. If QA outputs `PASS`, close the issue.
7. Repeat until all issues are completed.
8. 
