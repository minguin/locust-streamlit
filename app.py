import streamlit as st
import requests
import numpy as np
from datetime import datetime
import time

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# クエリパラメータを取得（各値はリストになっている）
query_params = st.query_params
# "action" キーが存在しない場合は、[""]（空文字列のリスト）を返す
action = query_params.get("action", [""])

st.title("クエリパラメータによるテスト実行")

if action == "fastapi":
    st.write("FastAPIバックエンドを呼び出します...")
    try:
        # FastAPIバックエンド（例: localhostのポート8000）へのGETリクエスト
        response = requests.get("http://localhost:8000/heavy_process")
        if response.status_code == 200:
            data = response.json()
            st.write(timestamp,"FastAPIからのレスポンス:",data)
            print(timestamp,"FastAPIからのレスポンス:",data)
        else:
            st.error(timestamp,"FastAPIバックエンドの呼び出しに失敗しました。")
            print(timestamp,"FastAPIバックエンドの呼び出しに失敗しました。")
    except Exception as e:
        st.error(timestamp,f"エラーが発生しました: {e}")
        print(timestamp,f"エラーが発生しました: {e}")

elif action == "local":
    st.write("ローカルの重い計算処理を実行します...")
    start_time = time.time()
    # 例として、1000×1000の行列積を計算（負荷をかけるための処理）
    n = 1000
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)
    C = np.dot(A, B)
    elapsed_time = time.time() - start_time
    st.write("計算完了！ 実行時間:", round(elapsed_time, 2), "秒")
    print(timestamp,"計算完了！ 実行時間:", round(elapsed_time, 2), "秒")
else:
    st.write("有効なアクションが指定されていません。URLに '?action=local' または '?action=fastapi' を追加してください。")
    print(timestamp,"有効なアクションが指定されていません。URLに '?action=local' または '?action=fastapi' を追加してください。")
