
import sys
import os
# Добавляем родительскую папку (serves_4) в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from src.albums.router import router as router_albums
from src.auth.router import router as router_auth
from src.admin.router import router as router_admin
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import FileResponse

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_albums)
app.include_router(router_auth)
app.include_router(router_admin)

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

if __name__ == "__main__":
    uvicorn.run('main:app', host = '127.0.0.1', port=8000, reload=True)