from fastapi import APIRouter, HTTPException, status
from typing import AnyStr, Dict
import json
import os

from services.dependencies import b64_to_docx, read_docx, parse_schedule, save_to_json

router = APIRouter()

@router.post("/api/post-lich-tuan")
def post_lich_tuan(data: Dict[AnyStr, AnyStr]):
    if not data:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Không có dữ liệu"
        )
    try:
        b64_to_docx(data["text"])
        text = read_docx()
        schedule = parse_schedule(text)
        save_to_json(schedule)
        return {"response": "Upload lịch tuần thành công!"}, 200
    except Exception as err:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = f"ERROR: {err}"
        )
@router.get("/api/get-lich-tuan")
def get_lich_tuan():
    current_path = os.getcwd()
    with open(os.path.join(current_path, "app", "data", "lichTuan", "lichTuan.json"), "rb") as file:
        return json.load(file), 200