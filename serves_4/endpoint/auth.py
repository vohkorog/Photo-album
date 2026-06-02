import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn
from fastapi import FastAPI, Cookie
from schemas.user import UserLoginScheme
from serveces.func import login_user
from fastapi.responses import JSONResponse, RedirectResponse


app = FastAPI()

@app.get('/')
def main_root():
    return f'root'

@app.get('/root')
def root(access_token: str = Cookie(None), user_id: str = Cookie(None), login: str = Cookie(None)):
    if not access_token:
        return RedirectResponse(url="/login", status_code=303)
    
    return {"message": f"Welcome {login}!", "user_id": user_id}

@app.post('/login')
def login(data: UserLoginScheme):
    user = login_user(
        login= data.username,
        password= data.password
    )

    response = RedirectResponse(url='/root')
    response.set_cookie(
        key="access_token",
        value=user["access_token"],
        httponly=True,  # Защита от XSS
        max_age=1800,   # 30 минут
        secure=False,   # True для HTTPS
        samesite="lax"
    )
    response.set_cookie(key="user_id", value=str(user["user_id"]))
    response.set_cookie(key="login", value=user["login"])
    
    return response
   

if __name__ == '__main__':
    uvicorn.run('auth:app', host= '127.0.0.1', port= 8000, reload= True)