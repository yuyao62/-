import pandas as pd
import json
import sys
import os

def excel_to_json(excel_file, output_file=None):
    # 讀取 Excel
    df = pd.read_excel(excel_file)

    # 自動偵測欄位名稱，並轉成字典
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
