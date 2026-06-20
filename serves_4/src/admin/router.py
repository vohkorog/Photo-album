import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter
from src.admin.services import db
from src.auth.services import user_db

router = APIRouter(prefix='/admin', tags = ['DEBUG'])

@router.post('/drop_all', summary='Пересоздание БД')
def drop_all():
    """Пересоздание БД с удалением старых записей"""
    db.delete_model()
    db.create_model()
    return f'Таблицы пересозданы'

@router.get('/all_users', summary='Вывод всех пользователей')
def all_users():
    users = user_db.get_all_users()
    return users