import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreateScheme(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLoginScheme(BaseModel):
    username: str
    password: str

class UserChangingPassScheme(BaseModel):
    old_password: str
    new_password: str

class UserChangingLoginScheme(BaseModel):
    new_login: str