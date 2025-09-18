import pandas as pd
import sqlite3

# CSVファイルをUTF-8として明示的に読み込む
df = pd.read_csv("data.csv", encoding="utf-8")

# SQLiteデータベースに保存
conn = sqlite3.connect("data.db")
df.to_sql("your_table_name", conn, if_exists="replace", index=False)
conn.close()
