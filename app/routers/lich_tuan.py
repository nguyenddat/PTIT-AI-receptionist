from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import AnyStr, Dict
import shutil
import json
import os

from services.dependencies import extract_events_from_doc, import_lichTuan 

router = APIRouter()
lichTuan = import_lichTuan()

@router.post("/api/post-lich-tuan")
def post_lich_tuan(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Không có dữ liệu"
        )
    if file.content_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file .docx")
    
    file_path = os.path.join(os.getcwd(), "app", "data", "lichTuan", "lichTuan.docx")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"response": "Upload file successfully"}, 200
    except Exception as err:
        raise HTTPException(status_code = HTTP_500_INTERNAL_SERVER_ERROR, detail = err )
    finally:
        extract_events_from_doc(file_path)
        lichTuan = import_lichTuan()

@router.get("/api/get-lich-tuan")
def get_lich_tuan():
    return lichTuan, 200