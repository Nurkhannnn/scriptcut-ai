# Project Plan: ScriptCut AI (Transcript-Based Video Editor)

## Overview
ScriptCut AI is a web application that allows users to edit videos by editing their text transcripts. Deleting a paragraph in the text editor automatically cuts the underlying video timeline.

## Target Users
- Content creators, podcasters, and video editors who want fast, text-based rough-cut video editing.

## Key Features (MVP)
1. **Project Management:** Create a project, upload video files and transcripts.
2. **Text-Based Editor Interface:** Interactive text view synced with a video player.
3. **Smart Cutting:** Deleting text blocks marks video segments as hidden/cut.
4. **Export:** Export the edited edit-decision list (EDL) or rendered video metadata.

## Tech Stack
- **Frontend:** React / Vite (interacting with a mock service layer first).
- **Backend:** Python + FastAPI.
- **Database & ORM:** SQLite with SQLAlchemy (DBMS-agnostic via ORM).
- **API Contract:** OpenAPI 3.0 (`openapi.yaml`).