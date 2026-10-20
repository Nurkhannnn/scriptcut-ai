# Brainstorming: ScriptCut AI (Transcript-Based Video Editor)

## Idea Selection
We chose a non-trivial, high-value SaaS idea: an AI-powered transcript-based video editor (similar to Descript). Users upload a video and its transcript, and editing the text automatically cuts the video timeline.

## Key Decisions & Scope
- **Target Audience:** Creators, podcasters, and editors looking for fast rough-cut editing via text.
- **Frontend:** React/Vite with Tailwind CSS, interacting with a centralized mock service layer first.
- **Backend:** Python with FastAPI.
- **Database & ORM:** SQLite with SQLAlchemy for data persistence (DBMS-agnostic via ORM).
- **API Contract:** OpenAPI 3.0 (`openapi.yaml`) defined between frontend and backend.