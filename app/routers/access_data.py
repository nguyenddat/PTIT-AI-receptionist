import os
import json
import logging
import uvicorn
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, AnyStr

from .dependencies import extract_data, import_data
from .dependencies import save_image, save_personal_data
from .face_recognition import model, TARGET_WEBSOCKET, manager, faces_data

router = APIRouter()

LOG = logging.getLogger(__name__)
LOG.info(uvicorn.Config.asgi_version)

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
        print(f"STATUS CODE: 503 / {err}")
        raise HTTPException(status_code = 503, detail = "err")

@router.post('/api/post-personal-img')
async def post_personal_img(
    data: Dict[AnyStr, Dict[AnyStr, List[AnyStr]] | Dict[AnyStr, AnyStr] | AnyStr]
    # DỮ LIỆU ĐƯỢC ĐỊNH DẠNG:
        # Dict(str: dict(str: list) || list(str) || str)
):
    global faces_data
    
    try:
        if not data:
            raise HTTPException(status_code = 504, detail = "Chưa có dữ liệu nào được nhận!")

        b64_img = data['b64_img']
        personal_data = data['cccd']
        name = personal_data['Name']
        role = data['role']
        personal_id = personal_data['Identity Code']
        personal_data.update({'role': role})

        save_img_path = os.path.join('./data/img', personal_id)
        if os.path.exists(save_img_path):
            raise HTTPException(status_code = 505, detail = "Thông tin của quý khách đã tồn tại!")
        else:
            os.makedirs(save_img_path)
        
        id = 0
        for img in b64_img:
            img_path = os.path.join(save_img_path, f'{name} {str(id)}.png')
            save_image(img, img_path)
            id += 1

        return {"response": "Upload successfully!"}, 200
    except Exception as err:
        print(f"STATUS CODE: 506 / {err}")
        raise HTTPException(status_code = 506, detail = err)
    finally:
        save_personal_data(save_img_path, model, personal_data)
        faces_data = import_data()
    
@router.get("/api/get-all-data")
async def get_all_data():
    try:
        return faces_data, 200
    except Exception as err:
        print(f"STATUS CODE: 507 / {err}")
        raise HTTPException(status_code = 507, detail = err)