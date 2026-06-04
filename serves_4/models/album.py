import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import text, String, ForeignKey, Integer
from typing import Annotated


time_now = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Base(DeclarativeBase):
    pass

class Album(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(text, nullable=True)
    create_at: Mapped[time_now]

    user: Mapped["UserModel"] = relationship(back_populates="albums")
    photos: Mapped[list["Photo"]] = relationship(back_populates="albums", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = "photos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer)
    content_type: Mapped[str] = mapped_column(String(100))
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id", ondelete="CASCADE"))
    uploaded_at: Mapped[time_now]
    
    # Связи
    album: Mapped["Album"] = relationship(back_populates="photos")