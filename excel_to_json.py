import pandas as pd
import json

# 你的 Excel
excel_path = "藥品藥代廠商統計_醫令統計_數量_20251211_114629.xlsx"
sheet_name = "Sheet1"

# 讀取 Excel
df = pd.read_excel(excel_path, sheet_name=sheet_name, engine="openpyxl")

# 整理欄位名稱
df.columns = df.columns.str.strip()

# 你之前提過：把「累計數量」改成「累計用量」
df.rename(columns={"累計數量": "累計用量"}, inplace=True)

# 修正資料
df["累計用量"] = pd.to_numeric(df["累計用量"], errors="coerce").fillna(0)
df["廠商"] = df["廠商"].fillna("未標示廠商")
df["藥品"] = df["藥品"].fillna("")
df["藥代"] = df["藥代"].fillna("")

# 轉成 JSON 格式
records = df[["藥代", "藥品", "廠商", "累計用量"]].to_dict(orient="records")

with open("inventory.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("🎉 已成功輸出 inventory.json，共 {} 筆資料".format(len(records)))
