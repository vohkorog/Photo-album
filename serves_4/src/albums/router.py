from fastapi import APIRouter, Depends
from src.albums.schemas import AlbumsCreateScheme
from src.auth.services import user_db
from src.albums.services import album_db


router = APIRouter(prefix="/albums", tags=["albums"])


@router.get('/')
def root():
    return f'root album'

@router.post('/create_albums')
def create_albums(data: AlbumsCreateScheme, current_user: dict = Depends(user_db.get_current_user_from_token)):
    album = album_db.create_album(
        title = data.title,
        description= data.description,
        user_id=current_user['id']
    )

    return album