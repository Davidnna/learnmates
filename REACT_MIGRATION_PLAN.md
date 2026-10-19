# LearnMeets AI React Migration — Milestone 1

## Goal
Introduce a modern React + Vite frontend while preserving the existing Flask backend, Groq integration, Neon PostgreSQL database, and student records.

## What is included in this milestone
- A separate `frontend/` Vite + React application.
- Responsive modern AI SaaS shell with sidebar, top navigation, dashboard, feature areas, help, settings, and authentication UI scaffolds.
- A shared fetch client configured to include credentials and accept a configurable `VITE_API_BASE_URL`.
- Vite local development proxy for `/api` requests to Flask on `127.0.0.1:5000`.
- Existing Flask templates and route handlers remain intact.

## Important integration status
This milestone establishes the frontend foundation; it does not yet replace the production HTML experience. The current Flask routes primarily return rendered HTML and use CSRF-protected form posts. The React forms and feature pages are intentionally scaffolds and are not represented as connected to the backend yet.

## Next milestone: API and authentication contract
Before feature activation, inspect each existing Flask route and implement/test appropriate JSON endpoints for:
- Session status and current student profile
- Registration, login, logout, and CSRF/session protection
- Dashboard summary and recent activity
- Tutor messages and conversation retrieval
- Document upload, listing, deletion, and extracted text availability
- Quiz generation, active quiz state, submission, score, history, and review
- Study-tool summary and flashcard generation
- Admin-only data with server-side authorization

Security requirements:
- Keep `GROQ_API_KEY`, `DATABASE_URL`, and `SECRET_KEY` exclusively on the server.
- Keep authorization and validation in Flask.
- Configure CORS narrowly if frontend and backend use separate origins; use secure cookie/session settings appropriate to deployment.
- Do not expose admin data or allow client-supplied user IDs to determine ownership.
- Preserve existing database tables and records; no destructive migration or database reset.

## Vercel and uploads
Vercel's `/tmp` is temporary and must not be treated as durable document storage. Confirm current document behavior and move persistent uploaded files to suitable external object storage before depending on uploaded files across invocations.

## Local development
1. Install Python requirements and configure a development `.env` as documented in the existing project README.
2. Start Flask on port 5000.
3. In `frontend/`, run `npm install` and `npm run dev`.
4. Keep production credentials out of frontend environment variables. Only public configuration such as `VITE_API_BASE_URL` belongs in the frontend.

## Acceptance gate before cutover
Test authentication and session expiry, tutor responses, upload/extraction, quiz counts and scoring, history/review, study tools, authorization boundaries, responsive layout, and existing student records. Keep the current deployment available until the new frontend is proven stable.
