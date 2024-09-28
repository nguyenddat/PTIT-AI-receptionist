import json
from typing import List, AnyStr
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from services.base_model import ConnectionManager
from services.dependencies import save_image, import_model, import_data, extract_data
from services.dependencies import face_recognition, detect_nums_of_people

router = APIRouter()
model = import_model()
manager = ConnectionManager()
TARGET_WEBSOCKET = None
faces_data = import_data()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global TARGET_WEBSOCKET
    global manager
    await manager.connect(websocket)
    TARGET_WEBSOCKET = websocket
    try:
        while True:
            data = await websocket.receive_text()
            save_image(data)
            nums_of_people = detect_nums_of_people('./services/received_img.png', model)
            if nums_of_people != 0:
                names = face_recognition('./services/received_img.png', model = model, faces_data = faces_data)
                await manager.send_response({
                    "key": "webcam", 
                    "value": {"nums_of_people": nums_of_people, "person_datas": names}}, websocket)
            else:
                await manager.send_response({
                    "key": "webcam", 
                    "value": {"nums_of_people": nums_of_people, "person_datas": []}}, websocket)
    except WebSocketDisconnect:
        TARGET_WEBSOCKET = None
    except Exception as err:
        raise HTTPException(status_code = 502, detail = err)

@router.post("/api/get-identity")
async def get_identity(
    data: List[AnyStr]
    # DỮ LIỆU ĐƯỢC ĐỊNH DẠNG:
        # list(str)
):
    global TARGET_WEBSOCKET, manager
    try:
        if not TARGET_WEBSOCKET:
            raise HTTPException(status_code = 503, detail = "Chưa có ai kết nối đến máy chủ!")
        
        decoded_data = extract_data(data)
        await manager.send_response({
            "key": "cccd",
            "value": json.dumps(decoded_data)
        }, TARGET_WEBSOCKET)
    except Exception as err:
        raise HTTPException(status_code = 503, detail = err)