# EdiVideo FastAPI Backend Starter

This backend matches the frontend starter routes.

## Features included
- Signup / login / current user
- Dashboard stats from database
- Project CRUD
- Avatar list + custom photo upload
- Mock video generation jobs
- Mock translation jobs
- SQLite persistence

## Run
```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on `http://127.0.0.1:8000`

## Frontend env
Set frontend `.env` to:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Important
Video generation and translation are mocked right now. They create jobs and return placeholder result URLs.
To make actual content creation real, connect external providers for:
- TTS
- Avatar rendering
- Video composition/export
- ASR + translation + dubbing
