# Vercel upload directory fix

The Flask app previously attempted to create `uploads/` inside `/var/task`, which is read-only on Vercel. The app now uses `/tmp/learnmeets_uploads` when the `VERCEL` environment variable is present, while keeping the existing project-local `uploads/` directory on Render and local development unless `UPLOAD_DIR` is explicitly configured.

The uploaded file is used for text extraction and removed immediately afterward; extracted document text is stored in the configured database. Vercel's `/tmp` storage is temporary and must not be treated as durable file storage.

## Deploy

1. Replace the corresponding `learnmates_ai/app.py` in your repository with this version.
2. Commit and push the change.
3. Redeploy the Vercel project.
4. Test the home page, login, upload and extraction of a small text/PDF file, AI tutoring, and quiz generation.

This change does not alter database settings or database contents. Keep the existing Render deployment available as a fallback.
