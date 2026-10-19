# LearnMeets AI Frontend

React + Vite foundation for the LearnMeets AI redesign.

## Start locally

```bash
npm install
npm run dev
```

The development server listens on `http://localhost:5173`. Its `/api` proxy points to Flask at `http://127.0.0.1:5000`.

To use a separately hosted Flask API, copy `.env.example` to `.env.local` and set `VITE_API_BASE_URL` to the API origin. Configure CORS and session cookies safely on the Flask service.

## Status
This is milestone 1: UI foundation and API client helper. Existing Flask pages remain unchanged. The login/register forms and feature screens are interface scaffolds until the matching authenticated JSON API endpoints are implemented and tested. Do not use this frontend as a production replacement yet.
