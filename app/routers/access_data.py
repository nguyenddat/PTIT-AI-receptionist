import os
from fastapi import APIRouter, HTTPException
from typing import Dict, List, AnyStr

from services.dependencies import import_data, png_to_base64
from services.dependencies import save_image, save_personal_data, get_face_embedding
from .face_recognition import model, faces_data

router = APIRouter()

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

        save_img_path = os.path.join('/home/rtx/Desktop/ai-team/PTIT-AI-receptionist/app/data/img', personal_id)
        if os.path.exists(save_img_path):
            raise HTTPException(status_code = 505, detail = "Thông tin của quý khách đã tồn tại!")
        else:
            os.makedirs(save_img_path)
        
        id = 0
        for img in b64_img:
            img_path = os.path.join(save_img_path, f'{name} {str(id)}.png')
            save_image(img, img_path)
            faces = get_face_embedding(img_path)
            if len(faces) != 1:
                return {"response": "Ảnh không đạt điều kiện!"}, 506
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
        data_return = []
        for face in faces_data:
            image_data = []
            identity_code = face["Identity Code"]
            path = os.path.join("/home/rtx/Desktop/ai-team/PTIT-AI-receptionist/app/data/img", identity_code)
            for file in os.listdir(path):
                if file.endswith('.png'):
                    image_data.append(png_to_base64(os.path.join(path, file)))
            data_return.append({
                "name": face["Name"],
                "identity_code": identity_code,
                "role": face["role"],
                "dob": face["DOB"],
                "gender": face["Gender"],
                "image_data": image_data
            })
        return data_return, 200
    except Exception as err:
        print(f"STATUS CODE: 507 / {err}")
        raise HTTPException(status_code = 507, detail = err)