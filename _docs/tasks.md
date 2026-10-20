# Backlog: ScriptCut AI MVP

## 1. Project Setup & Empty Test
Goal: Initialize the project repository structure with /frontend, /backend, and a passing test.
Description: Create directory structure, set up backend with pytest and frontend template, and ensure the initial test suite passes successfully.

## 2. Frontend Mock Implementation
Goal: Build a fully interactive frontend with mocked backend services.
Description: Create the React/Vite interface for transcript editing, video player sync, and text block deletion using a centralized mock service layer.

## 3. OpenAPI Contract Definition
Goal: Define the official API contract between frontend and backend.
Description: Analyze the frontend service layer and generate openapi.yaml at the repository root covering all endpoints for projects, transcripts, and edits.

## 4. FastAPI Backend with In-Memory Store
Goal: Implement a functional FastAPI backend matching openapi.yaml.
Description: Build routers, models, and an in-memory store with seeded data so the frontend can connect and fetch real responses.

## 5. SQLite Persistence and ORM Integration
Goal: Replace in-memory storage with SQLite and SQLAlchemy ORM.
Description: Implement database models, setup, and ensure data persists across application restarts.

## 6. End-to-End Integration and Testing
Goal: Connect frontend to FastAPI backend and verify the full user flow.
Description: Replace frontend mock service with real API calls, run end-to-end tests, and verify video transcript cutting logic.
