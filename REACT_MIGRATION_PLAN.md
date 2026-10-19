# LearnMeets AI React migration plan

## Milestone 1 — UI foundation
A separate React + Vite frontend, responsive application shell, and shared fetch client were introduced. The original Flask templates and handlers were retained.

## Milestone 2 — JSON API and feature wiring
This package adds authenticated Flask JSON endpoints and connects the React UI to them. Existing database models are reused; no destructive schema changes or database reset are included.

Implemented API areas:
- `GET /api/session` for authentication status and CSRF token.
- `POST /api/auth/register`, `/api/auth/login`, `/api/auth/logout`.
- `GET /api/dashboard` for account-specific metrics, recent quiz attempts, and materials.
- `GET/POST /api/chat` for conversation history and tutor messages.
- `GET/POST /api/materials` and `POST /api/materials/<id>/delete`.
- `GET /api/quiz/active`, `POST /api/quiz/generate`, and `POST /api/quiz/submit`.
- `GET /api/quiz-history` and `GET /api/quiz-history/<id>`.
- `GET/POST /api/study-tools` for summary and flashcard generation.

Security controls include session cookies, CSRF token validation for mutating requests, owner-scoped document/quiz queries, admin restrictions remaining server-side, and quiz answer keys withheld from the client before submission. Existing HTML routes remain intact.

## Before production cutover
1. Run local API smoke tests using a test account and verify login/logout/session behavior.
2. Test upload/extraction, AI chat, quiz generation/scoring, history review, and study tools.
3. Verify the existing Neon records remain present and unchanged.
4. Configure a stable `SECRET_KEY` on every backend deployment.
5. Prefer same-origin frontend/API routing. For separate origins, configure exact `FRONTEND_ORIGIN`, HTTPS, and appropriate cookie settings.
6. Vercel's `/tmp` is temporary; uploaded source files are removed after extraction in this prototype, while extracted text is stored in the database. Review privacy, size limits, and OCR provider availability.
7. Keep the old Flask UI available until the React feature set passes end-to-end checks.

## Verification limitation
This build workspace did not have all Python requirements installed, and `npm install` timed out. The backend source passed `py_compile`, but this is not a substitute for runtime integration tests or a Vite production build.
