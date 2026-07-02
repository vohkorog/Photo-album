import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends
from src.auth.services import user_db
from fastapi.responses import JSONResponse, RedirectResponse
from src.auth.schemas import UserLoginScheme, UserCreateScheme, UserChangingPassScheme, UserChangingLoginScheme

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post('/login', summary='Логирование пользователя')
def login(data: UserLoginScheme):
    user = user_db.login_user(
        login= data.username,
        password= data.password
    )
    return user

@router.post('/signin', summary='Регистрация пользователя')
def sigin(data: UserCreateScheme):
    user = user_db.register_user(
        login= data.username,
        email=data.email,
        password=data.password
    )    
    return f'Здравствуйте, {user.login}'

@router.patch('/change/pass', summary='Изменение пароля у пользователя')
def change_pass(data:UserChangingPassScheme, current_user: dict = Depends(user_db.get_current_user_from_token)):
    "Изменение пароля у пользователя"
    change = user_db.change_pass(user_login=current_user['login'],
                                 new_password=data.new_password,
                                 old_password=data.old_password, 
                                 user_id=current_user['id'])
    return change

@router.patch('/change/login', summary='Измненение логина')
def change_login(data: UserChangingLoginScheme, current_user: dict = Depends(user_db.get_current_user_from_token)):
    """Изменение логина у пользователя"""
    change = user_db.change_login(
        new_login=data.new_login,
        user_id=current_user['id'])
    return change