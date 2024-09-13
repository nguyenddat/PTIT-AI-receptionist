import numpy as np
import cv2
import json
import uvicorn

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from starlette.websockets import WebSocketDisconnect

from services.services import import_model, save_image 
from services.detect_nums_of_people import dectect_nums_of_people

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_response(self, response: dict, websocket: WebSocket):
        message = json.dumps(response)
        await websocket.send_text(message)

    async def broadcast(self, response: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(response))

model = import_model()
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            save_image(data)
            nums_of_people = dectect_nums_of_people('./services/received_image.png', model)
            await manager.send_response(response = {"nums_of_people": nums_of_people}, 
                                  websocket = websocket)
    except Exception as err:
        print(f'Error: {str(err)}')

@app.get('/')
async def root():
    return {"message": "websocket server is running. Connect to /ws for websocket communication"}

uvicorn.run(app, host = "192.168.10.14", port = 5050)