# Portfolio Frontend

React + Vite frontend for the personal portfolio. Deploy this folder to **Vercel** (or similar) with root directory set to `frontend` when using the monorepo.

## Setup

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Runs at `http://localhost:5173`. The Vite proxy forwards `/api` to your local backend (`http://127.0.0.1:8000`).

## Build

```bash
npm run build
```

Output is in `dist/`. Preview with:

```bash
npm run preview
```

## Environment

Copy `.env.example` to `.env` and set:

- **`VITE_API_BASE_URL`** – Backend API base URL (e.g. `https://your-api.onrender.com/api` for production). Required for production; optional for local dev if using the Vite proxy.

## Deployment (Vercel)

1. Connect the repo and set **Root Directory** to `frontend`.
2. Build command: `npm run build`
3. Output directory: `dist`
4. Add environment variable: `VITE_API_BASE_URL` = `https://<your-render-backend-url>/api`
