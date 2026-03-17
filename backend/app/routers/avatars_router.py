from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File
from ..auth import get_current_user
from ..models import User
from ..sample_data import AVATARS

router = APIRouter(prefix='/api/avatars', tags=['avatars'])

@router.get('')
def list_avatars(current_user: User = Depends(get_current_user)):
    return AVATARS

@router.post('/photo-avatar')
async def upload_photo_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    uploads_dir = Path('uploads/avatars')
    uploads_dir.mkdir(parents=True, exist_ok=True)
    save_path = uploads_dir / f'user_{current_user.id}_{file.filename}'
    save_path.write_bytes(await file.read())
    return {
        'message': 'Photo avatar uploaded',
        'avatar': {
            'id': f'custom-{current_user.id}',
            'name': 'Custom Avatar',
            'category': 'Custom',
            'preview_url': f'/{save_path.as_posix()}'
        }
    }
