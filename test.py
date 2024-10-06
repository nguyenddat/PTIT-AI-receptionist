import os
import time
import sqlite3
import pandas as pd
from datetime import datetime

def get_conn():
    conn = sqlite3.connect(os.path.join(os.getcwd(), "app", "database", "kiosk.db"))
    return conn

xls = pd.ExcelFile("./test.xlsx")
results = []
du_lieu_sv = [1]
du_lieu_lop_tin_chi = [0, 2, 3, 4, 5, 6, 7]
def insert():
    conn = get_conn()
    cursor = conn.cursor()
    cate : dict = None
    sinhvien = {}
    hocphan = {}
    loptinchi = {}
    nhomtinchi = {}
    sinhvien_nhomtinchi = {}
    id = 0
    for i in du_lieu_lop_tin_chi:
        if i == 0:
            cate = {
                0: ["SinhVien", "ma_sinh_vien"],
                1: ["SinhVien", "ho_ten"],
                2: ["SinhVien", "lop_hanh_chinh"],
                3: ["HocPhan", "ma_hoc_phan"],
                4: ["HocPhan", "ten_hoc_phan"],
                5: ["HocPhan", "so_tin_chi"],
                6: ["LopTinChi", "thu_tu_lop"],
                7: ['NhomTinChi', 'thu_tu_nhom'],
                8: ['LopTinChi', 'hoc_ky']
            }
        else:
            cate = {
                        0: ["SinhVien", "ma_sinh_vien"],
                        1: ["SinhVien", "ho_ten"],
                        2: ["SinhVien", "cccd"],
                        3: ["SinhVien", "lop_hanh_chinh"],
                        4: ["HocPhan", "ma_hoc_phan"],
                        5: ["HocPhan", "ten_hoc_phan"],
                        6: ["HocPhan", "so_tin_chi"],
                        7: ["LopTinChi", "thu_tu_lop"],
                        8: ['NhomTinChi', 'thu_tu_nhom'],
                        9: ['LopTinChi', 'hoc_ky']
                    }
        sheetname = xls.sheet_names[i]
        df = pd.read_excel(xls, sheetname, dtype = str)
        for index, row in df.iterrows():
            for col in df.columns:
                check = cate[id]
                table = check[0]
                temp = check[1]
                value = str(row[col])
                if value == 'nan' or temp == 'cccd':
                    if id == len(list(cate)) - 1:
                        id = 0
                    else:
                        id += 1
                    continue
                
                if table == 'SinhVien':
                    sinhvien.update({temp: value})
                if table == 'HocPhan':
                    if temp == "ma_hoc_phan":
                        loptinchi.update({temp: value})    
                    hocphan.update({temp: value})
                if table == 'LopTinChi':
                    loptinchi.update({temp: value})
                if table == 'NhomTinChi':
                    nhomtinchi.update({temp: value})
                    
                if id == len(list(cate)) - 1:
                    id = 0
                else:
                    id += 1
            if "ma_hoc_phan" in loptinchi.keys() and "thu_tu_lop" in loptinchi.keys():
                ma_lop_tin_chi = f'{loptinchi["ma_hoc_phan"]}-{loptinchi["thu_tu_lop"]}'
                loptinchi.update({"ma_lop_tin_chi": ma_lop_tin_chi})
                nhomtinchi.update({"ma_lop_tin_chi": ma_lop_tin_chi})
            
            if 'ma_lop_tin_chi' in nhomtinchi.keys():
                if 'thu_tu_nhom' in nhomtinchi.keys():
                    ma_nhom_tin_chi = f"{nhomtinchi['ma_lop_tin_chi']}-{nhomtinchi['thu_tu_nhom']}"
                else:
                    nhomtinchi.update({"thu_tu_nhom": "00"})
                    ma_nhom_tin_chi = f"{nhomtinchi['ma_lop_tin_chi']}"
                nhomtinchi.update({'ma_nhom_tin_chi': ma_nhom_tin_chi})
                sinhvien_nhomtinchi.update({'ma_nhom_tin_chi': ma_nhom_tin_chi})
                sinhvien_nhomtinchi.update({'ma_sinh_vien': sinhvien['ma_sinh_vien']})
                        
            if sinhvien == {} or hocphan == {} or loptinchi == {} or nhomtinchi == {} or sinhvien_nhomtinchi == {}:
                id = 0
                sinhvien = {}
                hocphan = {}
                loptinchi = {}
                nhomtinchi = {}
                sinhvien_nhomtinchi = {}
                continue
            
            cursor.execute('UPDATE SinhVien SET ho_ten = ?, lop_hanh_chinh = ? WHERE ma_sinh_vien = ?', (sinhvien['ho_ten'], sinhvien['lop_hanh_chinh'], sinhvien['ma_sinh_vien']))
            conn.commit()
            print(f"Luu thanh cong sinh vien {sinhvien['ma_sinh_vien']}")
            
            cursor.execute(f'''INSERT OR IGNORE
                        INTO HocPhan ({", ".join([x for x in hocphan.keys()])}) VALUES 
                        ({", ".join(["?" for _ in hocphan.keys()])})''', 
                        tuple(hocphan.values()))
            conn.commit()
            print(f"Luu thanh cong hoc phan {hocphan['ten_hoc_phan']}")
            
            
            cursor.execute(f'''INSERT OR IGNORE
                        INTO LopTinChi ({", ".join([x for x in loptinchi.keys()])}) VALUES 
                        ({", ".join(["?" for _ in loptinchi.keys()])})''', 
                        tuple(loptinchi.values()))
            conn.commit()
            print(f"Luu thanh cong lop tin chi {loptinchi['ma_lop_tin_chi']}")
            
            cursor.execute(f'''INSERT OR IGNORE 
                        INTO NhomTinChi ({", ".join([x for x in nhomtinchi.keys()])}) VALUES 
                        ({", ".join(["?" for _ in nhomtinchi.keys()])})''', 
                        tuple(nhomtinchi.values()))
            conn.commit()
            print(f"Luu thanh cong nhom tin chi {nhomtinchi['ma_nhom_tin_chi']}")

            cursor.execute(f'''INSERT OR IGNORE 
                        INTO SinhVien_NhomTinChi ({", ".join([x for x in sinhvien_nhomtinchi.keys()])}) VALUES 
                        ({", ".join(["?" for _ in sinhvien_nhomtinchi.keys()])})''', 
                        tuple(sinhvien_nhomtinchi.values()))
            
            conn.commit()
            print(f"Luu thanh cong sinh vien - nhom tin chi")

            print()
            sinhvien = {}
            hocphan = {}
            loptinchi = {}
            nhomtinchi = {}
            sinhvien_nhomtinchi = {}
            
    