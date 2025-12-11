import pandas as pd
import json
import sys
import os

# 欄位對應表：原始欄位名稱 → 標準欄位名稱
COLUMN_MAP = {
    "藥代": "藥品代碼",
    "代碼": "藥品代碼",
    "code": "藥品代碼",

    "藥品": "藥品名稱",
    "品名": "藥品名稱",
    "name": "藥品名稱",

    "廠商": "廠商",
    "供應商": "廠商",
    "vendor": "廠商",

    "累計數量": "盤點數量",
    "數量": "盤點數量",
    "qty": "盤點數量"
}

def normalize_columns(df):
    """將欄位名稱標準化"""
    new_columns = {}
    for col in df.columns:
        new_columns[col] = COLUMN_MAP.get(col.strip(), col.strip())
    return df.rename(columns=new_columns)

def excel_to_json(excel_file, output_file=None):
    # 讀取 Excel
    df = pd.read_excel(excel_file)

    # 欄位標準化
    df = normalize_columns(df)

    # 轉成 JSON 格式
    records = df.to_dict(orient="records")

    # 設定輸出檔名
    if output_file is None:
        base = os.path.splitext(excel_file)[0]
        output_file = base + ".json"

    # 寫入 JSON 檔案
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"✅ 已轉換完成：{output_file}")

# 命令列執行方式
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ 用法：python excel_to_json.py <Excel檔案路徑> [輸出檔名]")
    else:
        excel_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        excel_to_json(excel_file, output_file)
