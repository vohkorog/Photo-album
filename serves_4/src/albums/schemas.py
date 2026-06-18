
from pydantic import BaseModel
from datetime import datetime

class AlbumsCreateScheme(BaseModel):
    title: str
    description: str | None = None

class AlbumsDeleteScheme(BaseModel):
    id: int


class PhotoBase(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str

class PhotoScheme(PhotoBase):
    id: int
    album_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True