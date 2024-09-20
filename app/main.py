import uvicorn
from fastapi import Depends, FastAPI

from internal import admin 
from routers import face_recognition, access_data

app = FastAPI()

app.include_router(face_recognition.router)
app.include_router(access_data.router)

@app.get('/')
async def root():
    return {"message": "websocket server is running. Connect to /ws for websocket communication"}

uvicorn.run(app, host = "0.0.0.0", port = 1010)