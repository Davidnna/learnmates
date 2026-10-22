"""Static verification for the LearnMeets AI React-first migration.

Run from the repository root with: python scripts/verify_react_migration.py
This checks source wiring only; it does not replace browser/API integration tests.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
REACT = ROOT / "frontend" / "src" / "App.jsx"
CLIENT = ROOT / "frontend" / "src" / "api" / "client.js"
VERCEL = ROOT / "frontend" / "vercel.json"

checks = []

def check(label, condition, detail):
    checks.append((label, bool(condition), detail))

app = APP.read_text(encoding="utf-8")
react = REACT.read_text(encoding="utf-8")
client = CLIENT.read_text(encoding="utf-8")
vercel = VERCEL.read_text(encoding="utf-8")

check("React account route", 'path="/account"' in react and "function AccountPage" in react,
      "Account page is registered in React Router.")
check("Profile API wired", "updateAccount" in client and "api/account/profile" in client and '"/api/account/profile"' in app,
      "React client and Flask profile endpoint are present.")
check("Password API wired", "changePassword" in client and "api/account/password" in client and '"/api/account/password"' in app,
      "React client and Flask password endpoint are present.")
check("Notification bell absent from shared top bar", "Bell" not in react and "BellRing" not in react,
      "No bell icon import/reference was found in App.jsx.")
check("Back navigation implemented", "page-back-button" in react and "function goBack()" in react,
      "Top bar provides contextual back navigation.")
check("Credentialed API requests", "credentials: 'include'" in client,
      "API client includes browser credentials for session cookies.")
check("CSRF header wiring", "X-CSRF-Token" in client and "protect_state_changing_requests" in app,
      "Client sends CSRF header and Flask validates state-changing requests.")
check("Exact-origin credentialed CORS", "Access-Control-Allow-Credentials" in app and "FRONTEND_ORIGIN" in app,
      "Flask has explicit-origin credentialed CORS configuration.")
check("Legacy redirect preserves API routes", "request.path.startswith((\"/api/\", \"/static/\"))" in app and "REACT_FRONTEND_URL" in app,
      "Legacy browser route redirects are configurable and exclude API/static paths.")
check("Vercel SPA fallback", '"destination": "/"' in vercel,
      "Vercel rewrite sends client-side routes to the React entry point.")

for label, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'}: {label} — {detail}")
print(f"\n{sum(p for _, p, _ in checks)}/{len(checks)} static checks passed.")
sys.exit(0 if all(p for _, p, _ in checks) else 1)
