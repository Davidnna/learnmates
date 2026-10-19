# React public pages, route protection, 404 and loading update

## What changed

- Added a public landing page plus About, Features, How It Works, FAQ and Privacy pages.
- Kept sign-in and registration public; signed-in users are redirected to the dashboard from those pages.
- Added a session check at app startup and protected React workspace routes. Visitors who are not signed in are sent to `/login`.
- Added a global response to expired/invalid API sessions. The server already protects workspace JSON endpoints with Flask-Login; those checks remain in place.
- Added a branded 404 page for unknown frontend routes.
- Added a full-screen startup loader, in-page loading indicators and animated loading indicators on long-running action buttons.
- Added a Vercel SPA rewrite so client-side routes can load when opened directly or refreshed.
- No database schema changes, data resets, or migrations are included.

## Local validation

The JSX files passed the TypeScript parser check. A full Vite production build could not be confirmed in this environment because installing npm dependencies timed out. Run the following locally before deployment:

```powershell
cd frontend
npm install
npm run build
npm run dev
```

Test these scenarios: signed-out visits to `/dashboard`, `/tutor`, `/materials`, `/quizzes`, `/history`, and `/study-tools`; direct visits and refreshes on public pages; an unknown URL; successful sign-in and sign-out; a slow quiz generation; and a session expiry while on a protected page.

Keep the existing Neon database and current production deployment intact until the new frontend passes these checks.
