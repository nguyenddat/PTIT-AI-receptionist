import pandas as pd
import time
from datetime import datetime

xls = pd.ExcelFile("./test.xlsx")
results = []
du_lieu_sv = [1]
du_lieu_lop_tin_chi = [0, 2, 3, 4, 5, 6, 7]

from app.database.database import get_db
from app.database.models import SinhVien

import sqlite3

_ = {}
categories = [SinhVien.ma_sinh_vien, SinhVien.gioi_tinh, SinhVien.quoc_tich, SinhVien.dan_toc, SinhVien.ton_giao, SinhVien.ngay_sinh, SinhVien.cccd]
for i in du_lieu_sv:
    sheetname = xls.sheet_names[i]
    df = pd.read_excel(xls, sheetname, dtype = str)
    for index, row in df.iterrows():
        i = 0
        for col in df.columns:
            value = str(row[col])
            category = categories[i]
            if value == "nan":
                if i == 6:
                    i = 0
                else:   
                    i += 1
                continue
            if i == 5:
                value = datetime.strptime(value, "%d/%m/%Y").date()
            _.update({categories[i]: value})
            if i == 6:
                i = 0
            else:
                i += 1
        insert_into_table(SinhVien, _)
        print("Insert thanh cong: ", _[SinhVien.ma_sinh_vien])
        _ = {}
        time.sleep(1)