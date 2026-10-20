# Agent Guidelines: ScriptCut AI

## Commands

- `uv sync` - Install backend dependencies
- `uv run pytest` - Run backend test suite
- `npm --prefix frontend install` - Install frontend dependencies
- `npm --prefix frontend run dev` - Run frontend development server

## Documents

- `_docs/plan.md` - Project scope and specifications
- `_docs/process.md` - Development workflow and multi-agent lifecycle
- `_docs/tasks.md` - Backlog and task definitions
- Before grooming an issue, read `_docs/team/pm.md`
- Before implementing a task, read `_docs/team/software-engineer.md`
- Before verifying an issue, read `_docs/team/qa-engineer.md`

## Rules

- Tasks are tracked as GitHub Issues, worked on one at a time.
- Always check and fulfill all acceptance criteria before closing an issue.
- Ask for user approval before adding external dependencies.
- Commit regularly after every completed functional step.
