from fastapi import APIRouter, HTTPException
from typing import AnyStr
import json

from services.dependencies import b64_to_docx, read_docx, parse_schedule, save_to_json

router = APIRouter()

@router.post("/api/post-lich-tuan")
def post_lich_tuan(data: AnyStr):
    try:
        b64_to_docx(data)
        text = read_docx()
        schedule = parse_schedule(text)
        return {"response": "Upload lịch tuần thành công!"}, 200
    except:
        raise HTTPException(status_code = 508, detail = Exception)
    finally:
        save_to_json(schedule)

@router.get("/api/get-lich-tuan")
def get_lich_tuan():
    with open("/home/rtx/Desktop/ai-team/PTIT-AI-receptionist/app/data/lichTuan/lichTuan.json", "rb") as file:
        return json.load(file), 200