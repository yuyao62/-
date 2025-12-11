import pandas as pd
import json
import sys
import os

COLUMN_MAP = {
    "藥品代碼": "藥品代碼", "代碼": "藥品代碼", "code": "藥品代碼",
    "藥品名稱": "藥品名稱", "品名": "藥品名稱", "name": "藥品名稱",
    "盤點數量": "盤點數量", "數量": "盤點數量", "qty": "盤點數量",
    "廠商": "廠商", "供應商": "廠商", "vendor": "廠商",
    "盤點日期": "盤點日期", "日期": "盤點日期", "date": "盤點日期"
}

def normalize_columns(df):
    new_columns = {}
    for col in df.columns:
        new_columns[col] = COLUMN_MAP.get(col, col)
    return df.rename(columns=new_columns)

def excel_to_json(excel_file, output_file=None):
    df = pd.read_excel(excel_file)
    df = normalize_columns(df)
    records = df.to_dict(orient="records")

    if output_file is None:
        base = os.path.splitext(excel_file)[0]
        output_file = base + ".json"

    with open(output_file, "w", encoding="utf-8") as
        print("用法: python excel_to_json.py <excel檔案路徑> [輸出檔名]")
    else:
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        excel_to_json(excel_file, output_file)
