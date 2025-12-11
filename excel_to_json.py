import pandas as pd
import json
import sys
import os

# 欄位對應表：不同 Excel 欄位名稱 → 統一標準名稱
COLUMN_MAP = {
    "藥品代碼": "藥品代碼",
    "代碼": "藥品代碼",
    "code": "藥品代碼",

    "藥品名稱": "藥品名稱",
    "品名": "藥品名稱",
    "name": "藥品名稱",

    "盤點數量": "盤點數量",
    "數量": "盤點數量",
    "qty": "盤點數量",

    "廠商": "廠商",
    "供應商": "廠商",
    "vendor": "廠商",

    "盤點日期": "盤點日期",
    "日期": "盤點日期",
    "date": "盤點日期"
}

def normalize_columns(df):
    """將 Excel 欄位名稱統一成標準格式"""
    new_columns = {}
    for col in df.columns:
        if col in COLUMN_MAP:
            new_columns[col] = COLUMN_MAP[col]
        else:
            new_columns[col] = col  # 保留原始名稱
    df = df.rename(columns=new_columns)
    return df

def excel_to_json(excel_file, output_file=None):
    # 讀取 Excel
    df = pd.read_excel(excel_file)

    # 欄位名稱標準化
    df = normalize_columns(df)

    # 轉成字典
    records = df.to_dict(orient="records")

    # 如果沒有指定輸出檔名，就用原始檔名加上 .json
    if output_file is None:
        base = os.path.splitext(excel_file)[0]
        output_file = base + ".json"

    # 寫入 JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"✅ 已轉換完成：{output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python excel_to_json.py <excel檔案路徑> [輸出檔名]")
    else:
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        excel_to_json(excel_file, output_file)
