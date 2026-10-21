# LearnMeets AI — React-first migration

The React/Vite application in `frontend/` is the primary user interface. Flask remains the API/backend and retains its existing database, authentication/session logic, AI services, and legacy HTML routes for rollback.

For setup, Vercel deployment, Render environment variables, cross-origin cookie configuration, and rollback instructions, see `frontend/README.md`. Preserve the existing Neon database and all production secrets.
