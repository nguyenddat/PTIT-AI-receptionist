import pandas as pd
import os 
import numpy as np
import json

dataframe = pd.read_excel(os.path.join(os.getcwd(), "app", "data", "lichThucHanh", "lichThucHanh.xlsx"))

def extract_lichThucHanh_from_xlsx(file_path):
    xls = pd.ExcelFile(file_path)
    results = []
    for sheetname in xls.sheet_names:
        dataframe = pd. read_excel(xls, sheetname)

        dataframe = dataframe.iloc[3:].drop(dataframe.columns[0], axis = 1)

        headers = []
        cols_to_drop = []

        for i in range(len(dataframe.columns)):
            col = dataframe.columns[i]
            header = dataframe[col].iloc[0]
            
            if header in ("Ghi chú", "Tháng", "Hệ"):
                cols_to_drop.append(col)

        dataframe = dataframe.drop(columns = cols_to_drop)


        current_month: str = None
        for col in dataframe.columns:
            col_3_row = dataframe[col].iloc[0:3]
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
        result = []
        for index, row in dataframe.iterrows():
            _class = {}
            if index > 2:
                for i in range(len(dataframe.iloc[3:].columns)):
                    col = dataframe.columns[i]
                    
                    value = row.iloc[i]
                    if pd.isna(value):
                        continue
                        
                    
                    if headers[i] != "":
                        _class.update({headers[i]: value})
            result.append(_class)
        results += result[3:]
    with open(os.path.join(os.getcwd(), "app", "data", "lichThucHanh", "lichThucHanh.json"), 'w') as file:
        json.dump(results, file, ensure_ascii=False, indent = 4)

extract_lichThucHanh_from_xlsx(os.path.join(os.getcwd(), "app", "data", "lichThucHanh", "lichThucHanh.xlsx"))
