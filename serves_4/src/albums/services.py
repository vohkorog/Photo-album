
from src.models import Base, UserModel, AlbumModel
from src.database import engine, session_factory
from datetime import datetime
from src.security import get_password_hash, verify_password, create_access_token, decode_token
from sqlalchemy import select
from src.auth.services import user_db
    
class album_db:

    @staticmethod
    def create_album(title: str,
                     user_id: int,  
                     description: str | None = None, 
                     ):

        album = AlbumModel(
        title = title, 
        description = description,
        user_id = user_id
        )
        with session_factory() as session:
            session.add_all([album])
            session.commit()
            session.refresh(album)
        return album

    @staticmethod        
    def get_user_album(user_id: int):
        
        with session_factory() as session:
            query = (select(AlbumModel).where(AlbumModel.id == user_id))
            result = session.execute(query)
            album = result.scalars().all()
            return album

    
