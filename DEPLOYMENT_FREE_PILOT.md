# LearnMeets AI — zero-cost public pilot deployment

This configuration is intended for a small academic pilot, not a high-availability production service. Free hosting and AI quotas can sleep, pause, change, or be exhausted.

## Stack
- Web app: Render free web service (may sleep after inactivity; local disk is ephemeral).
- Database: Neon free PostgreSQL (create a project and copy its pooled or direct connection string as recommended by Neon; use SSL).
- AI: Groq API free tier for development/pilot use, subject to model availability and rate limits.
- Local development: SQLite and Ollama remain available.

## 1. Create a Neon PostgreSQL database
1. Create a project in Neon and create/select its database.
2. Copy the connection string from the Neon dashboard.
3. In Render, set `DATABASE_URL` to that full connection string. Keep it private. The app converts `postgresql://`/`postgres://` to SQLAlchemy's `postgresql+psycopg://` driver URL automatically.
4. Do not use Render's own free Postgres for permanent project data: its free database currently expires 30 days after creation.

## 2. Create a Groq API key
1. Create an account and API key in [Groq Console](https://console.groq.com/keys). Review the current free-plan limits and data-use terms.
2. In Render environment variables, set `GROQ_API_KEY` to the key. Do not put it in Git, HTML, JavaScript, screenshots, or a public issue.
3. Set `AI_PROVIDER=groq` and `GROQ_MODEL=openai/gpt-oss-20b`. Confirm the model remains available to your Groq account in the [supported models list](https://console.groq.com/docs/models). Optionally set `GROQ_FALLBACK_MODEL` only to another model you have verified in Groq Console.
4. Free-plan limits can be reached and can change. Do not send sensitive personal, assessment, or confidential institutional information unless the applicable terms and institutional approval allow it.

## 3. Deploy to Render
1. Push this folder to a Git repository. Never commit `.env`, real keys, a local database, or student data.
2. In Render, choose **New > Web Service** and connect the `learnmates` GitHub repository. Configure the service directly in the Render dashboard; this project intentionally does not use a Blueprint file.
3. Confirm the service is on the Free plan.
4. Set `DATABASE_URL`, `GROQ_API_KEY`, and a strong `SECRET_KEY` in the Render dashboard. Keep all secrets out of GitHub.
5. Deploy and wait for `/health` to return `{"status":"ok"}`.
6. Register a test account; test chat, quiz generation, uploads, logout/login, and saved history after a redeploy.

## 4. Important persistence note
The app stores extracted document text in PostgreSQL, but the original uploaded PDF/TXT file is stored under `uploads/`, which is ephemeral on Render Free. Most app features use the stored extracted text; however, original uploads will not persist across restarts/redeploys. For a real launch, either add object storage (for example, an S3-compatible bucket) or change the app to delete the temporary file after extraction and treat the extracted text as the permanent saved content. This package does not automatically add object storage.

## 5. Before making the URL widely public
- Add rate limiting to registration, login, chat, and quiz-generation endpoints.
- Add email verification and password reset; document how users can request account/data deletion.
- Review privacy notices and institutional approval before collecting real student data.
- Add database backups and a tested restore procedure.
- Add malware scanning and safer storage/isolation for uploaded files.
- Use schema migrations (such as Flask-Migrate/Alembic) before changing database models. `db.create_all()` creates missing tables but does not migrate existing tables.
- Do not promote an admin user through public registration. Set the admin role through a secure, one-time database operation.
- Test provider failures and quota exhaustion. A free AI quota can stop responses until it resets.

## Environment variables

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random secret set in Render; keep private |
| `DATABASE_URL` | Neon PostgreSQL connection string |
| `AI_PROVIDER` | `groq` |
| `GROQ_API_KEY` | Secret from Groq Console |
| `GROQ_MODEL` | `openai/gpt-oss-20b` (verify availability) |
| `GROQ_FALLBACK_MODEL` | Optional second model verified in Groq Console; leave blank otherwise |
| `AI_TIMEOUT_SECONDS` | `60` |
| `COOKIE_SECURE` | `true` |
| `FLASK_DEBUG` | `false` |

## Render URL note

The default `onrender.com` hostname is based on the Render service name. To try to use `https://learnmates.onrender.com`, open the existing web service in the Render Dashboard and rename it to `learnmates` if that name is available. Render may keep the old URL or require creating a new service depending on the service state; verify the hostname shown in Settings before sharing it. The requested name is not guaranteed to be available.
