from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import pandas as pd
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_PATH = "database.db"

@app.get("/", response_class=HTMLResponse)
def scatter_chart(request: Request):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM data", conn)
    conn.close()

    # 対象列（利益率以外）
    base_columns = [
        "売上高", "営業利益", "経常利益", "純利益", "ROE", "ROA"
    ]

    # 数値に変換
    for col in base_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 必要最小限のデータがない行を除去
    df = df.dropna(subset=["企業名", "売上高"])

    # 売上高0除外（利益率がNaNや無限になるのを防止）
    df = df[df["売上高"] > 0]

    # 利益率を計算
    df["営業利益率"] = df["営業利益"] / df["売上高"] * 100
    df["経常利益率"] = df["経常利益"] / df["売上高"] * 100
    df["純利益率"]   = df["純利益"] / df["売上高"] * 100

    # 散布図の軸候補
    axis_options = [
        "売上高", "営業利益", "経常利益",
        "営業利益率", "経常利益率", "純利益", "純利益率",
        "ROE", "ROA"
    ]

    # JSON化して渡す
    data_json = json.dumps(df.to_dict(orient="records"), ensure_ascii=False)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data_json": data_json,
        "axis_options": axis_options
    })
