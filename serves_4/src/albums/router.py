from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from src.albums.schemas import AlbumsCreateScheme, AlbumsDeleteScheme, PhotoScheme, PhotoDeleteScheme, GetAlbums
from src.auth.services import user_db
from src.albums.services import album_db, photo_db


router = APIRouter(prefix="/albums", tags=["albums"])


@router.post('/create_albums', response_model = AlbumsCreateScheme, summary="Создание альбома")
def create_albums(data: AlbumsCreateScheme, 
                  current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    """Создание альбома у пользователя"""
    album = album_db.create_album(
        title = data.title,
        description= data.description,
        user_id=current_user['id']
    )
    return album

@router.get('/get_albums', summary="Получение альбомов")
def get_albums(current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Поулчение всех альбомов пользователей у авторезированного пользователя"""
    try:
        albums = list(album_db.get_user_albums(current_user['id']))
        return albums
    except:
        return f'неправельный токен'
    
@router.delete('/delete_album', summary="Удаление альбома")
def delete_album(data: AlbumsDeleteScheme, 
                current_user: dict = Depends(user_db.get_current_user_from_token)):
    
    """Удаление альбома оп id у авторезированно пользователя"""
    album = album_db.delete_user_album(user_id = current_user['id'], id= data.id)
    return f'Альбом успешно удален {album}'

@router.post('/{album_id}/photos', response_model=PhotoScheme, summary="Добавление фото к альбому")
def add_photo(albums_id: int, 
              current_user: dict = Depends(user_db.get_current_user_from_token), 
              file: UploadFile = File(...)):
    
    """Добавление по id альбома у авторезированного пользователя"""
    photo = photo_db.upload_photo(user_id=current_user['id'], album_id=albums_id, file = file)
    return photo

@router.delete('/delete_photos', response_model=PhotoDeleteScheme, summary="Удаление фото у альбома")
def delete_photo(data: PhotoDeleteScheme,
                 current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Удаление фото по id у авторезированного пользователя"""
    photo_db.delete_photo(photo_id=data.id, user_id=current_user['id'])
    return f'Фото с id {data.id} удалено'


@router.get('/get_photos_album', summary="Получение метаданных всех фото у абльбома")
def get_photos_alum(album_id: int, 
                    current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение метаданных всех фото по id альбома у авторезированного пользователя"""
    photos = photo_db.get_album_photo(album_id=album_id, user_id=current_user['id'])
    return photos

@router.get('/photos/{photo_id}/file', summary="Получение изобрадение фото")
def get_photo_file(photo_id: int, current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение изображения фото по id у авторезированного пользователя"""
    photo = photo_db.get_photo(photo_id=photo_id, user_id=current_user['id'])
    
    return FileResponse(
        path=photo.file_path,
        media_type=photo.content_type,
        filename=photo.filename
    )

@router.post('/set_share_album', summary="Поделиться альбомом")
def set_share_album(shared_user_id: int, 
                shared_album_id: int, 
                current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Поделится альбомом с другим пользователем по id альбома и id пользователя"""
    album_db.shared_album(shared_album_id=shared_album_id, shared_user_id=shared_user_id, ownre_id=current_user['id'])
    return f'Альбом с id - {shared_album_id} для пользователя {shared_user_id} успешно присвоен'

@router.get('/get_shared_albums', summary="Получение общего альбома")
def get_shared_albums(
    shared_album_id: int,
    current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение общего альбома по id у пользователя, с которым поделились альбомом"""
    album = album_db.get_shared_album(shared_album_id=shared_album_id, shared_user_id=current_user['id'])
    return album

@router.get('/get_all_shared_albums', summary="Получение всех общих альбомов у пользователя")
def get_all_shared_albums(current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Получение всех общих альбомов пользователя"""
    albums = album_db.get_all_shared_album(shared_user_id=current_user['id'])
    return albums