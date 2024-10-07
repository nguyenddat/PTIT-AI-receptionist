from fastapi import APIRouter, HTTPException, status, UploadFile, File
from typing import AnyStr, Dict
import shutil
import json
import os

from services.dependencies import extract_lichThucHanh_from_xlsx, import_lichThucHanh

router = APIRouter()
lichTuan = import_lichThucHanh()

@router.post("/api/post-lich-thuc-hanh")
def post_lich_thuc_hanh(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Không có dữ liệu"
        )
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file .xlsx")
    
    file_path = os.path.join(os.getcwd(), "app", "data", "lichThucHanh", "lichThucHanh.xlsx")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"response": "Upload file successfully"}, 200
    except Exception as err:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = err )
    finally:
        extract_lichThucHanh_from_xlsx(file_path)
        lichTuan = import_lichThucHanh()

@router.get("/api/get-lich-thuc-hanh")
def get_lich_tuan():
    return lichTuan, 200