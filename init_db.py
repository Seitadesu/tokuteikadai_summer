import sqlite3
import pandas as pd

# Shift_JISで読み込む（Excel等で出力したCSVに対応）
df = pd.read_csv("data.csv", encoding="shift_jis")

# SQLiteデータベースへ接続（ファイルなければ自動作成）
conn = sqlite3.connect("database.db")

# テーブル名 'data' に保存（既存あれば置き換え）
df.to_sql("data", conn, if_exists="replace", index=False)

conn.close()

print("✅ データベースにインポート完了")
