import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers.auth_router import router as auth_router
from .routers.projects_router import router as projects_router
from .routers.dashboard_router import router as dashboard_router
from .routers.avatars_router import router as avatars_router
from .routers.translate_router import router as translate_router
from .routers.videos_router import router as videos_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='EdiVideo API', version='0.1.0')

frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

uploads_dir = Path('uploads')
uploads_dir.mkdir(exist_ok=True)
app.mount('/uploads', StaticFiles(directory='uploads'), name='uploads')

@app.get('/')
def root():
    return {'message': 'EdiVideo backend is running'}

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(dashboard_router)
app.include_router(avatars_router)
app.include_router(translate_router)
app.include_router(videos_router)
