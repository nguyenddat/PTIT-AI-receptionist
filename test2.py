import pandas as pd
from datetime import datetime, timedelta
import time
import os 
import sqlite3

def get_conn():
    return sqlite3.connect(os.path.join(os.getcwd(), "app", "database", "kiosk.db"))

xls = pd.ExcelFile("./test3.xlsx")

def exact_time(tiet_bat_dau: int, so_tiet: int):
    gio_hoc = {}
    tiet = 1
    start = 7
    while tiet <= 16:
        if tiet == 5:
            start = 12
        gio_bat_dau = f'{start}h'
        gio_ket_thuc = f'{start}h50'
        gio_hoc.update({tiet: f'{gio_bat_dau} - {gio_ket_thuc}'})
        tiet += 1
        start += 1

    gio_bat_dau = gio_hoc[tiet_bat_dau].split(" - ")[0]
    gio_ket_thuc = gio_hoc[tiet_bat_dau + so_tiet].split(" - ")[1]
    return gio_bat_dau, gio_ket_thuc

def exact_day(text: str, thu: int):
    ngay_bat_dau, ngay_ket_thuc = map(str, text.split(" - "))
    ngay_bat_dau = datetime.strptime(ngay_bat_dau, "%d/%m/%y")
    ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, "%d/%m/%y")

    ngay_chinh_xac = ngay_bat_dau + timedelta(thu - 2)
    return ngay_chinh_xac.strftime("%d/%m/%Y")

cates = {
    "Mã môn học": "ma_hoc_phan",
    "Tên môn học/ học phần": "ten_hoc_phan",
    "Nhóm": "thu_tu_lop",
    "Tổ TH": "thu_tu_nhom",
    "Thứ": "thu",
    "Tiết BĐ": "tiet_bat_dau",
    "Số tiết": "so_tiet",
    "Phòng": "phong",
    "Mã giảng viên mới": "ma_can_bo",
    "Giảng viên giảng dạy": "ho_ten"
}

lich_hoc = []
for i in range(len(xls.sheet_names)):
    sheetname = xls.sheet_names[i]
    df = pd.read_excel(xls, sheetname, dtype = str)
    df = df.iloc[8:, :-15]

    headers = []
    cols_to_drop = []

    for i in range(len(df.columns)):
        col = df.columns[i]
        header = df[col].iloc[0]
        
        if header in ("TT", "Tổ hợp", "Kíp", "Nhà", "Ghi chú", "Tháng", "Hệ", "Khoa", "Bộ môn", "Hình thức thi"):
            cols_to_drop.append(col)

    df = df.drop(columns = cols_to_drop)
    current_month: str = None
    for col in df.columns:
        col_3_row = df[col].iloc[0:3]
        first_cell = col_3_row.iloc[0]
        second_cell =  col_3_row.iloc[1]
        third_cell = col_3_row.iloc[2]
        
        if not pd.isna(first_cell):
            current_month = first_cell
            if not pd.isna(second_cell) and second_cell != first_cell:
                if not pd.isna(third_cell) and third_cell != second_cell:
                    headers.append("-".join([str(second_cell), str(third_cell), str(first_cell)]))
                else:
                    headers.append("-".join([str(second_cell), str(first_cell)]))
            else:
                headers.append(str(first_cell))
        else:
            first_cell = current_month
            if not pd.isna(second_cell) and second_cell != first_cell:
                if not pd.isna(third_cell) and third_cell != second_cell:
                    headers.append("-".join([str(second_cell), str(third_cell), str(first_cell)]))
                else:
                    headers.append("-".join([str(second_cell), str(first_cell)]))
            else:
                headers.append("")

    for i in range(len(headers)):
        header = headers[i]
        if "-" not in header:
            continue
        header = header.split()[0]
        temp = header.split("-")
        try:
            if len(temp) != 3:
                ngay_bat_dau, ngay_ket_thuc, nam, thang = temp[0], temp[1], temp[4], temp[3]
            else:    
                ngay_bat_dau, ngay_ket_thuc, thang_nam = temp[0], temp[1], temp[2].split("/")
                thang, nam = thang_nam[0], thang_nam[1]

            bat_dau  = f'{ngay_bat_dau}/{thang}/{nam}'
            if int(ngay_ket_thuc) < int(ngay_bat_dau):
                if int(thang) + 1 > 12:
                    thang, nam = "1", f"{int(nam) + 1}" 
                else:
                    thang = f"{int(thang) + 1}"
            ket_thuc = f'{ngay_ket_thuc}/{thang}/{nam}' 
            headers[i] = f'{bat_dau} - {ket_thuc}'
        except:
            print(header)
    df = df.iloc[4:]

    for index, row in df.iterrows():
        id = 0
        thu: int = None
        tiet_bat_dau: int = None
        so_tiet: int = None
        time: str = None
        startTime: str = None 
        endTime: str = None
        temp = {}
        lich = []
        for col in df.columns:
            value = row[col]
            ca = headers[id]
            if ca in cates.keys():
                ca = cates[ca]
                if ca == "thu_tu_nhom" and pd.isna(value):
                    value = "00"
                if ca == "thu":
                    thu = int(value)
                    id += 1
                    continue
                if ca == "tiet_bat_dau":
                    tiet_bat_dau = int(value)
                if ca == "so_tiet":
                    so_tiet = int(value)
                if tiet_bat_dau and so_tiet:
                    startTime, endTime = exact_time(tiet_bat_dau, so_tiet)
                    temp.update({"startTime": startTime})
                    temp.update({"endTime": endTime})
                temp.update({ca: value})
            else:
                if pd.isna(value):
                    id += 1
                    continue
                day = exact_day(ca, thu)
                lich.append(day)
            id += 1
        temp.update({"day": lich})
        lich_hoc.append(temp)

p = 0
conn = get_conn()
cursor = conn.cursor()
for i in range(len(lich_hoc)):
    temp = lich_hoc[i]
    ma_lop_tin_chi = f"{temp['ma_hoc_phan']}-{temp['thu_tu_lop']}"
    canbo = {
        "ma_can_bo": temp["ma_can_bo"],
        "ho_ten": temp["ho_ten"]
    }
    canbo_loptinchi = {
        "ma_can_bo": temp["ma_can_bo"],
        "ma_lop_tin_chi": ma_lop_tin_chi
    }
    thu_tu_nhom = temp['thu_tu_nhom']
    if thu_tu_nhom == "00":
        ma_nhom_tin_chi = f"{ma_lop_tin_chi}"
    else:
        ma_nhom_tin_chi = f"{ma_lop_tin_chi}-{temp['thu_tu_nhom']}"
    nhom_tin_chi = {
        "ma_nhom_tin_chi": ma_nhom_tin_chi,
        "ma_lop_tin_chi": ma_lop_tin_chi,
        "thu_tu_nhom": thu_tu_nhom
    }

    cursor.execute(f'''INSERT OR IGNORE
                    INTO nhomtinchi ({", ".join([_ for _ in nhom_tin_chi.keys()])}) VALUES
                    ({", ".join(["?" for _ in nhom_tin_chi.keys()])})''', 
                    tuple(nhom_tin_chi.values()))
    conn.commit()

    for lich in temp["day"]:
        thuc_hanh = {
            "id": p,
            "ma_nhom_tin_chi": ma_nhom_tin_chi,
            "ngay_hoc": lich,
            "tiet_bat_dau": temp['tiet_bat_dau'],
            "so_tiet": temp['so_tiet'],
            "gio_bat_dau": temp['startTime'],
            "gio_ket_thuc": temp['endTime']
        }    

        cursor.execute(f'''INSERT OR IGNORE
                       INTO lichhoc ({", ".join([_ for _ in thuc_hanh.keys()])}) VALUES
                       ({", ".join(["?" for _ in thuc_hanh.keys()])})''', 
                       tuple(thuc_hanh.values()))
        conn.commit()
        print(f'INSERT THANH CONG {thuc_hanh["ma_nhom_tin_chi"]}')
        p += 1
conn.close()

            
    