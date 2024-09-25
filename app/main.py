import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal import admin 
from routers import face_recognition, access_data, lich_tuan, auth
from database.database import engine, Base 

app = FastAPI()
Base.metadata.create_all(bind = engine)

app.include_router(face_recognition.router)
app.include_router(access_data.router)
app.include_router(lich_tuan.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ['*'],
    allow_credentials = ['*'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get('/')
async def root():
    return {"message": "websocket server is running. Connect to /ws for websocket communication"}

uvicorn.run(app, host = "0.0.0.0", port = 5050)