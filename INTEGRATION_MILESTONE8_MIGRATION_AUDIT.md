# Milestone 8 — React-first migration audit

## Scope
This milestone audits the uploaded Milestone 7 source package and adds a repeatable static verification script. It does not replace the production database, alter the database schema, change student records, or change secret values.

## Static findings
- React Router registers `/account` and renders the account-management page.
- The React API client calls Flask profile and password endpoints.
- The shared React top bar has contextual back navigation.
- No bell icon import/reference was found in `frontend/src/App.jsx`.
- The API client includes credentials and sends the CSRF header for state-changing requests.
- Flask has CSRF validation, exact-origin credentialed CORS, and configurable legacy-page redirects that exclude API/static paths.
- Vercel has an SPA rewrite for client-side routes.

## Repeatable check
From the repository root run:

```bash
python scripts/verify_react_migration.py
python -m py_compile app.py scripts/verify_react_migration.py
```

The static verifier checks source wiring only. It does not prove that browser cookies, deployed CORS, external AI requests, file uploads, or all UI flows work end to end.

## Current verification status
- ZIP integrity: passed.
- Python syntax compilation: passed.
- Static migration checks: 10/10 passed.
- React production build: not verified; `npm install --no-audit --no-fund` timed out in this environment.
- Flask test suite: blocked because Flask is not installed in the audit runtime (`ModuleNotFoundError: No module named 'flask'`). This is an environment/dependency limitation, not a passing test result.
- Live browser/deployment tests: not run.

## Required staging tests before production cutover
Test registration, login persistence after refresh, logout, account profile changes, password changes, chat, materials upload/delete, quiz generation/submission/history, study tools, direct route refreshes, and legacy redirects. Inspect browser Network requests and Render logs for cookie, CORS, CSRF, and API errors.

## Safety
Keep the existing `SECRET_KEY`, `DATABASE_URL`, AI credentials, and production student data unchanged. Do not reset or recreate the database. Keep `REACT_FRONTEND_URL` unset until the deployed React app has been tested, so the legacy Flask interface remains available as a rollback path.

## Git commit message
`test: add React migration verification checks`
