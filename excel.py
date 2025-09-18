import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# スプレッドシートAPI用のスコープと認証
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials.json', scope)  # ← JSONファイル名
client = gspread.authorize(creds)

# スプレッドシートのURLから開く
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1bVnRGxmzUDbs6yKzFJARPikzCOMF8Q1o5pJsVjX3dPI/edit#gid=0')

# 「kigyou」シートを開く（もしくは index=0 で最初のシート）
worksheet = spreadsheet.worksheet('kigyou')

# データを取得してDataFrameに変換
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # ヘッダー行付き

# D列（4番目の列）をチェックし、「- 」を含む行を削除
df_filtered = df[df.iloc[:, 3] != '- ']

# ワークシートの内容を一度クリア
worksheet.clear()

# フィルタ済みデータを再度アップロード
worksheet.update([df.columns.values.tolist()] + df_filtered.values.tolist())
