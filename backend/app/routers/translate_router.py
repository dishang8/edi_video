from pathlib import Path
from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db, SessionLocal
from ..models import VideoJob, User
from ..schemas import JobCreate, JobOut
from ..auth import get_current_user

router = APIRouter(prefix='/api/translate', tags=['translate'])

def finish_translate_job(job_id: int, db_factory):
    db = db_factory()
    try:
        job = db.get(VideoJob, job_id)
        if not job:
            return
        job.status = 'completed'
        job.progress = 100
        job.result_url = f'https://example.com/translated/video-job-{job.id}.mp4'
        job.message = 'Mock translation completed'
        db.add(job)
        db.commit()
    finally:
        db.close()

@router.post('/upload')
async def upload_video(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    uploads_dir = Path('uploads/translations')
    uploads_dir.mkdir(parents=True, exist_ok=True)
    save_path = uploads_dir / f'user_{current_user.id}_{file.filename}'
    save_path.write_bytes(await file.read())
    return {'message': 'File uploaded', 'file_path': save_path.as_posix()}

@router.post('/start', response_model=JobOut)
def start_translation(payload: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = VideoJob(owner_id=current_user.id, job_type='translate', status='processing', progress=55, message=f"Translating to {payload.target_language or 'selected language'}")
    db.add(job)
    db.commit()
    db.refresh(job)
    background_tasks.add_task(finish_translate_job, job.id, SessionLocal)
    return job

@router.get('/{job_id}/status', response_model=JobOut)
def get_translation_status(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.get(VideoJob, job_id)
    if not job or job.owner_id != current_user.id or job.job_type != 'translate':
        raise HTTPException(status_code=404, detail='Job not found')
    return job

@router.get('/{job_id}/result')
def get_translation_result(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.get(VideoJob, job_id)
    if not job or job.owner_id != current_user.id or job.job_type != 'translate':
        raise HTTPException(status_code=404, detail='Job not found')
    return {'result_url': job.result_url, 'status': job.status}
