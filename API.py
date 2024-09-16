import json
import numpy as np
import random
import uvicorn

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from services.services import import_model, save_image
from services.detect_nums_of_people import get_face_embedding, detect_nums_of_people, face_recognition

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

def import_data():
    roles = ["Nhân viên", "Sinh viên"]
    positions = ["Nhân viên", "Sinh viên", "Trưởng phòng", "Giảng viên"]
    departments = ["Phòng nghiên cứu và phát triển Công nghệ số", "Công nghệ định hướng ứng dụng", "Học viện công nghệ bưu chính viễn thông", "Khách"]
    id = 1

    faces_data = [
        ("Nguyễn Trường Giang", get_face_embedding("./data/giang.png", model = model)),
        ("Nguyễn Trường Giang", get_face_embedding("./data/giang2.jpg", model = model)),
        ("Nguyễn Trường Giang", get_face_embedding("./data/giang3.jpg", model = model)),
        ("Đức Định", get_face_embedding("./data/dinh.jpg", model = model)),
        ("Đức Định", get_face_embedding("./data/dinh2.jpg", model = model)),
        ("Đăng Sang", get_face_embedding("./data/dangsang.jpg", model = model)),
        ("Đăng Sang", get_face_embedding("./data/dangsang2.jpg", model = model)),
        ("Đăng Sang", get_face_embedding("./data/dangsang3.jpg", model = model)),
        ("Đăng Sang", get_face_embedding("./data/dangsang4.jpg", model = model)),
        ("Đăng Sang", get_face_embedding("./data/dangsang5.jpg", model = model)),
        ("Nam", get_face_embedding("./data/nam.jpg", model = model)),
        ("Nam", get_face_embedding("./data/nam2.jpg", model = model)),
        ("Nam", get_face_embedding("./data/nam3.jpg", model = model)),
        ("Đạt", get_face_embedding("./data/IMG_4050.JPG", model = model))
    ]

    for i in range(len(faces_data)):
        person = faces_data[i]

        res = {
            "id": id,
            "name": person[0],
            "embedding": person[1] if person[1] is not None else [np.zeros(512)]
        }
        role = random.choice(roles)
        res.update({"role": role})
        
        position = random.choice(positions)
        res.update({"position": position})

        department = random.choice(departments)
        res.update({"department": department})
        
        faces_data[i] = res

    return faces_data

faces_data = import_data()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            save_image(data)
            nums_of_people = detect_nums_of_people('./services/received_image.png', model)
            if nums_of_people != 0:
                names = face_recognition('./services/received_image.png', model = model, faces_data = faces_data)
                await manager.send_response({"nums_of_people": nums_of_people, "person_datas": names}, websocket)
            else:
                await manager.send_response({"nums_of_people": nums_of_people, "person_datas": []}, websocket)
    except Exception as err:
        print(f'Error: {err}')

@app.get('/')
async def root():
    return {"message": "websocket server is running. Connect to /ws for websocket communication"}

uvicorn.run(app, host = "192.168.10.12", port = 5050)