from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, VideoJob, User
from ..schemas import JobCreate, JobOut
from ..auth import get_current_user

router = APIRouter(prefix='/api/videos', tags=['videos'])

def finish_job(job_id: int, db_factory):
    db = db_factory()
    try:
        job = db.get(VideoJob, job_id)
        if not job:
            return
        job.status = 'completed'
        job.progress = 100
        job.result_url = f'https://example.com/generated/video-job-{job.id}.mp4'
        job.message = 'Mock video generation completed'
        if job.project_id:
            project = db.get(Project, job.project_id)
            if project:
                project.status = 'completed'
                project.last_output_url = job.result_url
                db.add(project)
        db.add(job)
        db.commit()
    finally:
        db.close()

@router.post('/generate', response_model=JobOut)
def generate_video(payload: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if payload.project_id is not None:
        project = db.get(Project, payload.project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail='Project not found')
        project.status = 'rendering'
        db.add(project)

    job = VideoJob(owner_id=current_user.id, project_id=payload.project_id, job_type='generate', status='processing', progress=65, message='Generating video...')
    db.add(job)
    db.commit()
    db.refresh(job)

    from ..database import SessionLocal
    background_tasks.add_task(finish_job, job.id, SessionLocal)
    return job

@router.get('/{job_id}/status', response_model=JobOut)
def get_video_status(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.get(VideoJob, job_id)
    if not job or job.owner_id != current_user.id or job.job_type != 'generate':
        raise HTTPException(status_code=404, detail='Job not found')
    return job

@router.get('/{job_id}/result')
def get_video_result(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.get(VideoJob, job_id)
    if not job or job.owner_id != current_user.id or job.job_type != 'generate':
        raise HTTPException(status_code=404, detail='Job not found')
    return {'result_url': job.result_url, 'status': job.status}
