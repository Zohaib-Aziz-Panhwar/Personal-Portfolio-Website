# Personal Portfolio

An elegant, responsive personal portfolio with a **React (Vite)** frontend and **FastAPI** backend, designed for easy deployment: frontend on Vercel, backend on Render, database on MongoDB Atlas.

## Project Structure

```
personal portfolio/
├── frontend/          # React + Vite app → deploy to Vercel
│   ├── src/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .env.example
│   └── README.md      # Frontend setup & Vercel deployment
├── backend/           # FastAPI app → deploy to Render
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── requirements.txt
│   ├── routes/
│   └── .env            # Your env (not committed); use Render env vars in prod
└── README.md           # This file
```

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
# Set MONGODB_URL etc. in backend/.env
uvicorn main:app --reload
```

API: `http://127.0.0.1:8000`, docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App: `http://localhost:5173`. Vite proxy sends `/api` to the backend.

## Deployment

| Part      | Host        | Root directory | Notes |
|-----------|-------------|----------------|--------|
| Frontend  | **Vercel**  | `frontend`     | Set `VITE_API_BASE_URL` to your Render API URL + `/api`. See `frontend/README.md`. |
| Backend   | **Render**  | `backend`      | Web Service, Python; start: `uvicorn main:app --host 0.0.0.0 --port $PORT`. Add `MONGODB_URL`, CORS for Vercel URL. |
| Database  | **MongoDB Atlas** | —        | Use connection string in Render env; allow `0.0.0.0/0` for Render. |

See **frontend/README.md** for Vercel steps and env vars. Backend expects `MONGODB_URL`, `MONGODB_DB_NAME`, and optional SMTP vars (see `backend/config.py`).

## Features

- 🎨 Warm palette, deep teal accents, responsive layout
- 📱 Sections: Hero, About, Projects, Education, Certifications, Blog, Contact
- ⚡ React Query, lazy routes, Vite proxy for local API
- 🔌 Axios API layer in `frontend/src/services/api.js`
- 🛡️ Admin area for content (optional)

## Tech Stack

- **Frontend:** React 18, Vite, React Router, TanStack Query, Axios
- **Backend:** FastAPI, PyMongo, Uvicorn
- **Database:** MongoDB (Atlas)

## License

MIT
