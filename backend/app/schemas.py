from datetime import datetime
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {'from_attributes': True}

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    user: UserOut

class ProjectCreate(BaseModel):
    title: str = 'Untitled Project'
    script: str = ''
    avatar_id: str | None = None
    voice: str = 'Ava'
    language: str = 'en-US'
    background: str | None = None
    resolution: str = '1080p'
    format: str = 'mp4'
    subtitles: bool = True
    status: str = 'draft'

class ProjectUpdate(BaseModel):
    title: str | None = None
    script: str | None = None
    avatar_id: str | None = None
    voice: str | None = None
    language: str | None = None
    background: str | None = None
    resolution: str | None = None
    format: str | None = None
    subtitles: bool | None = None
    status: str | None = None
    last_output_url: str | None = None

class ProjectOut(BaseModel):
    id: int
    owner_id: int
    title: str
    script: str
    avatar_id: str | None
    voice: str
    language: str
    background: str | None
    resolution: str
    format: str
    subtitles: bool
    status: str
    last_output_url: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}

class DashboardStats(BaseModel):
    projects: int
    translations: int
    generated_videos: int
    render_success: float

class JobCreate(BaseModel):
    project_id: int | None = None
    source_language: str | None = None
    target_language: str | None = None
    title: str | None = None

class JobOut(BaseModel):
    id: int
    job_type: str
    status: str
    progress: int
    result_url: str | None
    message: str | None

    model_config = {'from_attributes': True}
