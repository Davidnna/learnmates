# LearnMeets AI React frontend — integration milestone 2

React + Vite interface connected to the existing Flask application through authenticated JSON endpoints. The original Flask HTML routes remain available as a rollback path.

## Local development

1. In the project root, activate your Python virtual environment and install the project requirements:
   `python -m pip install -r requirements.txt`
2. Configure `.env` with your existing `DATABASE_URL`, a stable `SECRET_KEY`, and the AI provider key. Do not commit `.env`.
3. Start Flask from the project root: `python app.py` (default port 5000).
4. In `frontend/`, run `npm install` and `npm run dev`. Open `http://localhost:5173`. The Vite proxy forwards `/api` requests to Flask.

## Connected features

- Session-aware registration and login, with a session CSRF token.
- Dashboard metrics and recent quiz attempts.
- AI tutor chat with optional document grounding.
- Document upload, extracted-text listing, and owner-checked deletion.
- Quiz generation, server-side active quiz storage, submission and scoring. Correct answers are kept on the server until submission.
- Quiz history and review.
- Summary and flashcard generation from an owned learning material.

## Deployment notes

Prefer serving the frontend and API on the same site or through a same-origin reverse proxy. If using separate origins, set `VITE_API_BASE_URL` in `frontend/.env.local` to the Flask API origin and set `FRONTEND_ORIGIN` on Flask to the exact frontend origin. For genuinely cross-site cookies, set `COOKIE_SECURE=true` and `SESSION_COOKIE_SAMESITE=None`; use HTTPS on both origins. Do not use wildcard CORS with credentialed sessions. Browser third-party-cookie restrictions can still affect cross-site sessions, so same-origin routing is preferred.

Set a stable secret on the server. Keep `DATABASE_URL`, `GROQ_API_KEY`, and `SECRET_KEY` server-side; never prefix them with `VITE_`. Preserve the existing Neon database and records. This package does not reset or migrate existing tables.

## Validation status

The Flask source passed Python syntax compilation in the build workspace. A full Flask runtime/API test and Vite production build could not be completed here because the environment lacks several Python dependencies and `npm install` timed out. Run the verification checklist in `INTEGRATION_MILESTONE2.md` in your local project before changing production routing.
