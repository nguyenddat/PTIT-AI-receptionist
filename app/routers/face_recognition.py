import logging
import uvicorn
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from .base_model import ConnectionManager
from .dependencies import save_image, import_model, import_data
from .dependencies import face_recognition, detect_nums_of_people

router = APIRouter()
model = import_model()
manager = ConnectionManager()
TARGET_WEBSOCKET = None
faces_data = import_data()


LOG = logging.getLogger(__name__)
LOG.info(uvicorn.Config.asgi_version)

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
            nums_of_people = detect_nums_of_people('./routers/received_image.png', model)
            if nums_of_people != 0:
                names = face_recognition('./routers/received_image.png', model = model, faces_data = faces_data)
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
        LOG.error(err)
