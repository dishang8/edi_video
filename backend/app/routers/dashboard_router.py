from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Project, VideoJob, User
from ..schemas import DashboardStats
from ..auth import get_current_user

router = APIRouter(prefix='/api/dashboard', tags=['dashboard'])

@router.get('/stats', response_model=DashboardStats)
def stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).count()
    translations = db.query(VideoJob).filter(VideoJob.owner_id == current_user.id, VideoJob.job_type == 'translate').count()
    generated = db.query(VideoJob).filter(VideoJob.owner_id == current_user.id, VideoJob.job_type == 'generate').count()
    successful = db.query(VideoJob).filter(VideoJob.owner_id == current_user.id, VideoJob.status == 'completed').count()
    total_jobs = db.query(VideoJob).filter(VideoJob.owner_id == current_user.id).count()
    render_success = 100.0 if total_jobs == 0 else round((successful / total_jobs) * 100, 1)
    return DashboardStats(projects=projects, translations=translations, generated_videos=generated, render_success=render_success)
