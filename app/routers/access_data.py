import os
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, AnyStr

from services.dependencies import import_data, png_to_base64
from services.dependencies import save_image, save_personal_data, get_face_embedding
from .face_recognition import model, faces_data

router = APIRouter()

@router.post('/api/post-personal-img')
async def post_personal_img(
    data: Dict[AnyStr, List[AnyStr] | Dict[AnyStr, AnyStr] | AnyStr]
    # DỮ LIỆU ĐƯỢC ĐỊNH DẠNG:
        # Dict(str: dict(str: list) || list(str) || str)
):
    global faces_data
    if not data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Không có dữ liệu"
        )
    b64_img = data['b64_img']
    personal_data = data['cccd']
    name = personal_data['Name']
    role =  data['role']
    personal_id = personal_data['Identity Code']
    personal_data.update({'role': role})
    
    current_path = os.getcwd()
    save_img_path = os.path.join(current_path, "app", "data", "img", personal_id)
    if os.path.exists(save_img_path):
        return {"response": "Request thành công"}, 200
    
    os.makedirs(save_img_path)
    try:
        id = 0 
        for img in b64_img:
            print(name)
            img_path = os.path.join(save_img_path, f'{name} {id}.png')
            save_image(img, img_path)
            print(f"Lưu thành công ảnh: {name} {id}.png")
            with open(os.path.join(save_img_path, f'{name} {id} base64.txt'), 'w') as file:
                file.write(img)
            id += 1
        save_personal_data(save_img_path, model, personal_data)
        faces_data = import_data()
        return {"response": "Request thành công"}, 200
    except Exception as err:
        os.rmdir(save_img_path)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = f"ERROR: {err}"
        )
        
@router.get("/api/get-all-data")
async def get_all_data():
    from collections import defaultdict
    import json

    current_path = os.getcwd()    
    normalized_data = defaultdict(lambda: {
        "embedding": [],
        "Identity Code": None,
        "Name": None,
        "DOB": None,
        "Gender": None,
        "role": None
    })

    for entry in faces_data:
        identity_code = entry["Identity Code"]
        normalized_data[identity_code]["identity_code"] = entry["Identity Code"]
        normalized_data[identity_code]["name"] = entry["Name"]
        normalized_data[identity_code]["dob"] = entry["DOB"]
        normalized_data[identity_code]["gender"] = entry["Gender"]
        normalized_data[identity_code]["role"] = entry["role"]

    final_data = list(normalized_data.values())

    for i in range(len(final_data)):
        person = final_data[i]
        identity = person["identity_code"]
        b64 = []
        path = os.path.join(os.getcwd(), "app", "data", "img", identity)
        for file in os.listdir(path):
            if file.endswith("base64.txt"):
                with open(os.path.join(path, file), 'r') as file:
                    b64.append(file.read())
        person["b64"] = b64
        final_data[i] = person
    print(final_data[1])
    return final_data, 200